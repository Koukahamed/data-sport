pip install -U isort black flake8 pylint | out-null
isort musculation dags | out-null
black musculation dags --quiet
flake8 musculation
pylint musculation
