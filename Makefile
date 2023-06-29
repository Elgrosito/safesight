install_dependencies:
	pip install -r requirements.txt

local_test:
	export DB_CONNECTION_STATUS=$$? && \
	uvicorn main:app --port 8200 --log-level debug --reload

clean:
	@rm -fr */__pycache__
