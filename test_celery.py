from tasks.task import test_task

result = test_task.delay("Garvit")

print("Task ID:", result.id)