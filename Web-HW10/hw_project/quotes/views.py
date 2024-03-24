from django.shortcuts import render, redirect
from django.core.paginator import Paginator
# Create your views here.
from .utils import get_mongodb
from .forms import TagForm, NoteForm
from .models import Tag, Quote
from django.shortcuts import render, redirect, get_object_or_404



def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_age = 10
    paginator = Paginator(list(quotes), per_age)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})



def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


def note(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/note.html', {"tags": tags, 'form': form})

    return render(request, 'quotes/note.html', {"tags": tags, 'form': NoteForm()})


