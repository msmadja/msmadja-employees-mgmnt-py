install-deps:
	uv sync

serve:
	uv run uvicorn main:app --reload

test:
	pytest