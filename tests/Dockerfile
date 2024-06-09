FROM fastapi-image

WORKDIR /tests/

COPY poetry.lock pyproject.toml /tests/

RUN poetry config virtualenvs.create false && poetry install

COPY . .

RUN chmod u+x commands.sh

CMD ["/bin/sh", "/tests/commands.sh"]