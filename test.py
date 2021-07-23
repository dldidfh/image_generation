from hangul_romanize import Transliter
from hangul_romanize.rule import academic

transliter = Transliter(academic)
print(transliter.translit(u'안녕하세요'))