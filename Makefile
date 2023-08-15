COMPOSE=compose


up:
	docker $(COMPOSE) up

down:
	docker $(COMPOSE) down

build:
	docker $(COMPOSE) build