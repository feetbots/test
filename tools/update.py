from tooltils.errors import ConnectionError
from tooltils.requests import get
from sys import exit


class update:
    def vcheck(self) -> list:
        url: str = 'https://api.github.com/repos/feetbots/tooltils/releases?per_page=100'
        try:
            data: dict = get(url).json
        except ConnectionError:
            throw()
        return [[i['tag_name'][1:].split('-')[0], i['name']] for i in data]

    def check(self, cver: str) -> str:
        for i in self.vcheck():
            if cver == i:
                pass
            for x in [0, 1, 2]:
                if int(i[0].split('.')[x]) > int(cver.split('.')[x]):
                    return i

        return False

    def update(self, cver: str, ver: str) -> None:
        pass
