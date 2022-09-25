import pytest
from peewee import MySQLDatabase


@pytest.fixture(scope="session")
def docker_compose_command():
    return "docker compose"


@pytest.fixture(scope="session")
def docker(docker_services):
    def test_mysql():
        try:
            mysql_db = MySQLDatabase(None)
            mysql_db.init(
                'test', user='root', password='mysql', host="localhost", port=3306
            )
            mysql_db.connect()
            return mysql_db.is_connection_usable()
        except:
            return False

    docker_services.wait_until_responsive(timeout=60, pause=1, check=test_mysql)

    docker_services.wait_until_responsive(
        timeout=60,
        pause=1,
        check=lambda: docker_services.port_for("redis", 6379) is not None,
    )
