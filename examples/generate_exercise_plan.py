"""
This example demonstrates how to use Goose to plan an exercise routine.

Exercise planning is a good use case because it demonstrates the need for tasks to depend on the outputs of other tasks.
You have your initial flow input, which is your overall fitness goals, and that's the starting point for morning exercise.
Then afternoon exercise is planned considering both your goals and morning workout.
Finally, evening exercise is planned considering your goals and previous workouts of the day.
"""

import asyncio

from goose import Agent, FlowArguments, Result, flow, task
from goose.agent import AIModel, SystemMessage, TextMessagePart, UserMessage


class FitnessGoals(FlowArguments):
    goals: list[str]


class Workout(Result):
    routine_name: str
    exercises: list[str]
    duration_minutes: int
    reason: str


@task
async def plan_morning_workout(*, goals: list[str], agent: Agent) -> Workout:
    formatted_goals = "\n".join(f"- {goal}" for goal in goals)
    suggested_workout = await agent(
        messages=[
            UserMessage(
                parts=[
                    TextMessagePart(
                        text=f"What exercises should I do in the morning? Here are my fitness goals:\n{formatted_goals}"
                    )
                ]
            ),
        ],
        system=SystemMessage(
            parts=[
                TextMessagePart(
                    text=(
                        "You are a helpful fitness trainer that plans morning workouts based on fitness goals. "
                        "Suggest a workout routine that takes 15-45 minutes. "
                        "Explain why you chose these exercises."
                    )
                )
            ]
        ),
        response_model=Workout,
        model=AIModel.GEMINI_FLASH,
        task_name="morning_workout",
    )
    return suggested_workout


@task
async def plan_afternoon_workout(*, goals: list[str], morning: Workout, agent: Agent) -> Workout:
    formatted_goals = "\n".join(f"- {goal}" for goal in goals)
    formatted_morning = f"Morning workout: {morning.routine_name} ({', '.join(morning.exercises)})"
    suggested_workout = await agent(
        messages=[
            UserMessage(
                parts=[
                    TextMessagePart(text=f"What exercises should I do in the afternoon? Here are my fitness goals:\n{formatted_goals}"),
                    TextMessagePart(text=f"Here was my morning workout:\n{formatted_morning}"),
                ]
            ),
        ],
        system=SystemMessage(
            parts=[
                TextMessagePart(
                    text=(
                        "You are a helpful fitness trainer that plans afternoon workouts based on fitness goals. "
                        "Consider the morning workout when planning the afternoon routine. "
                        "Suggest a workout that takes 15-45 minutes. "
                        "Explain why you chose these exercises."
                    ),
                )
            ]
        ),
        response_model=Workout,
        model=AIModel.GEMINI_FLASH,
        task_name="afternoon_workout",
    )
    return suggested_workout


@task
async def plan_evening_workout(*, goals: list[str], afternoon: Workout, morning: Workout, agent: Agent) -> Workout:
    formatted_goals = "\n".join(f"- {goal}" for goal in goals)
    formatted_morning = f"Morning workout: {morning.routine_name} ({', '.join(morning.exercises)})"
    formatted_afternoon = f"Afternoon workout: {afternoon.routine_name} ({', '.join(afternoon.exercises)})"
    suggested_workout = await agent(
        messages=[
            UserMessage(
                parts=[
                    TextMessagePart(
                        text=f"What exercises should I do in the evening? Here are my fitness goals:\n{formatted_goals}"
                    ),
                    TextMessagePart(text=f"Here was my morning workout:\n{formatted_morning}"),
                    TextMessagePart(text=f"Here was my afternoon workout:\n{formatted_afternoon}"),
                ]
            ),
        ],
        system=SystemMessage(
            parts=[
                TextMessagePart(
                    text=(
                        "You are a helpful fitness trainer that plans evening workouts based on fitness goals. "
                        "Consider the morning and afternoon workouts when planning the evening routine. "
                        "Suggest a workout that takes 15-45 minutes. "
                        "Explain why you chose these exercises."
                    ),
                )
            ]
        ),
        response_model=Workout,
        model=AIModel.GEMINI_FLASH,
        task_name="evening_workout",
    )
    return suggested_workout


@flow
async def exercise_plan(*, flow_arguments: FitnessGoals, agent: Agent) -> None:
    morning = await plan_morning_workout(goals=flow_arguments.goals, agent=agent)
    afternoon = await plan_afternoon_workout(goals=flow_arguments.goals, morning=morning, agent=agent)
    await plan_evening_workout(goals=flow_arguments.goals, afternoon=afternoon, morning=morning, agent=agent)


async def main() -> None:
    print("\nExample fitness goals:")
    print("- lose weight")
    print("- build muscle")
    print("- improve cardio")
    print("- increase flexibility")
    print("- reduce stress")
    print("\nEnter your fitness goals one at a time.")
    print("Press Enter without typing anything when you're done.\n")
    
    goals = []
    while True:
        goal = input("Enter a fitness goal: ").strip()
        if not goal:
            break
        goals.append(goal)
    
    if not goals:
        print("No goals entered, using default goals...")
        goals = ["build muscle", "improve cardio"]
    
    fitness_goals = FitnessGoals(goals=goals)
    async with exercise_plan.start_run(run_id="my-exercise-plan") as run:
        await exercise_plan.generate(fitness_goals)

    morning = run.get(task=plan_morning_workout).result
    afternoon = run.get(task=plan_afternoon_workout).result
    evening = run.get(task=plan_evening_workout).result

    print(f"\nMorning Workout: {morning.routine_name} ({morning.duration_minutes} minutes)")
    for exercise in morning.exercises:
        print(f"  - {exercise}")
    print(f"Reasoning: {morning.reason}")
    print("---")
    print(f"Afternoon Workout: {afternoon.routine_name} ({afternoon.duration_minutes} minutes)")
    for exercise in afternoon.exercises:
        print(f"  - {exercise}")
    print(f"Reasoning: {afternoon.reason}")
    print("---")
    print(f"Evening Workout: {evening.routine_name} ({evening.duration_minutes} minutes)")
    for exercise in evening.exercises:
        print(f"  - {exercise}")
    print(f"Reasoning: {evening.reason}")


if __name__ == "__main__":
    asyncio.run(main()) 