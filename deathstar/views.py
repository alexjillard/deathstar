from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from deathstar.models import Planet

from deathstar.models import Charge


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "deathstar/home.html",
        {}
    )

def charge(request):
    c = Charge.objects.active()
    c.increment()

    return render(
        request,
        "deathstar/charging.html",
        {
            'charge': c,
            'segments': '█' * int(c.percent / 10),
            'partial': '░' if c.percent % 10 else '',
            'spaces': ' ' * int(10 - c.percent / 10),
        }
    )

@require_POST
def fire(request):
    c = Charge.objects.active()
    if request.htmx and c.charged:
        c.use_charge()

        current_planet = Planet.objects.active()
        current_planet.destroy()

        return render(
            request,
            "deathstar/planet-boom.html"
        )
    else:
        return HttpResponse(request, {'message': 'Wait for full charge'},  status=423) # 423 locked

def jump(request):
    # TODO: gotta jump to the new planet
    print('jump')

@require_GET
def planet(request):
    current_planet = Planet.objects.active()

    return render(
        request,
        "deathstar/planet.html",
        {'planet_name': current_planet.name},
    )
