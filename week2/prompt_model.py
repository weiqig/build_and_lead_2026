import sys
import requests
# import subprocess

def prompt_model(model: str, prompt: str) -> str :
	response = requests.post(
		"http://localhost:11434/api/generate",
		json={
			"model": model,
			"prompt": prompt,
			"stream": False
		}
	)

	data = response.json()
	return data.get("response", "")

def main() -> None:
	models = ['llama3.1', 'phi3', 'deepseek-r1:1.5b']
	if len(sys.argv) != 3:
		print("Usage: uv run prompt_model.py <model> <prompt>")
		return
	try:
		model = sys.argv[1]
		prompt = sys.argv[2]
		if model not in models:
			raise ValueError(f"Invalid model provided!\nModels available: {models}")
		response = prompt_model(model, prompt)
		print(response)
	except Exception as e:
		print(e)


if __name__ == "__main__":
	main()