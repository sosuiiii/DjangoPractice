from .models import Work

from timewire.models import Work
def gett(self):
    w = Work.objects.get(name="コロワイド")
    print(w)