from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader

from myapp.forms import UserCreateForm, DodajStranForm, UporabnikUpdateForm, SlikaUploadForm
from .models import UporabnikProfil, Stran
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.contrib.auth.models import Group, User


def index(request):
    return render(request, 'myapp/index.html', {
        'is_supervisor': request.user.groups.filter(name='Nadzorniki').exists(),
        'is_prosilec': request.user.groups.filter(name='Prosilci').exists(),
        'strani_seznam': Stran.objects.all()
    })


@login_required
def profil(request, username):
    if str(username) != str(request.user):
        return redirect('myapp:index')

    uporabnik_form = UporabnikUpdateForm(request.POST or None, instance=request.user)
    slika_form = SlikaUploadForm(request.POST or None, request.FILES or None, instance=request.user)

    if request.method == 'POST':
        if 'profil_update' in request.POST:
            if uporabnik_form.is_valid():
                user = uporabnik_form.save()
                return redirect('myapp:profil', username)

        if 'slika_update' in request.POST:
            if slika_form.is_valid():
                u = UporabnikProfil.objects.get(uporabnik=request.user)
                u.slika_profila = request.FILES['slika_profila']
                u.save()
                return redirect('myapp:profil', username)

    return render(request, 'myapp/profil.html', {
        'is_supervisor': request.user.groups.filter(name='Nadzorniki').exists(),
        'is_prosilec': request.user.groups.filter(name='Prosilci').exists(),
        'uporabnik_form': uporabnik_form,
        'slika_form': slika_form,
        'strani_seznam': Stran.objects.all()
    })



def stran(request, stran_id):
    stran_x = get_object_or_404(Stran, pk=stran_id)

    return render(request, 'myapp/iskana_stran.html', {
        'id': stran_x.id,
        'naslov': stran_x.naslov,
        'vsebina': stran_x.vsebina,
        'avtorslika': stran_x.avtor.slika_profila,
        'avtorupor': stran_x.avtor.uporabnik,
        'avtor': stran_x.avtor.uporabnik.get_full_name(),
        'datum': str(stran_x.datum_nastanka.day) + ". " + str(stran_x.datum_nastanka.month) + ". " +
                 str(stran_x.datum_nastanka.year) + " ob " + str(stran_x.datum_nastanka.hour) + ":" + str(
            stran_x.datum_nastanka.minute),
        'is_supervisor': request.user.groups.filter(name='Nadzorniki').exists(),
        'is_prosilec': request.user.groups.filter(name='Prosilci').exists(),
        'strani_seznam': Stran.objects.all()
    })


@login_required
def dodajStran(request):
    if request.method == 'POST':
        form = DodajStranForm(request.POST)
        if form.is_valid():
            nova_stran = form.save(commit='False')
            nova_stran.avtor = UporabnikProfil.objects.get(uporabnik=request.user)
            nova_stran.datum_nastanka = timezone.now()
            nova_stran.save()
            return redirect('myapp:stran', stran_id=nova_stran.id)
    else:
        form = DodajStranForm()
        return render(request, 'myapp/dodaj.html', {
            'form': form,
            'strani_seznam': Stran.objects.all(),
            'is_supervisor': request.user.groups.filter(name='Nadzorniki').exists(),
            'is_prosilec': request.user.groups.filter(name='Prosilci').exists()
        })


def uredi(request, stran_id):
    post = get_object_or_404(Stran, id=stran_id)
    if request.method == "POST":
        form = DodajStranForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit='False')
            post.avtor = post.avtor
            post.datum_nastanka = timezone.now()
            post.save(force_update=True)
            return redirect('myapp:stran', stran_id=post.id)
    else:
        form = DodajStranForm(instance=post)
    return render(request, 'myapp/uredi.html', {
        'form': form,
        'id': post.id,
        'strani_seznam': Stran.objects.all(),
        'is_supervisor': request.user.groups.filter(name='Nadzorniki').exists(),
        'is_prosilec': request.user.groups.filter(name='Prosilci').exists()
    })


class IzbrisiStranView(DeleteView):
    model = Stran
    success_url = reverse_lazy('myapp:index')

    template_name = 'myapp/stran_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(IzbrisiStranView, self).get_context_data(**kwargs)
        context['is_supervisor'] = self.request.user.groups.filter(name='Nadzorniki').exists()
        context['is_prosilec'] = self.request.user.groups.filter(name='Prosilci').exists()
        context['avtorupor'] = get_object_or_404(Stran, pk=self.kwargs['pk']).avtor.uporabnik
        context['strani_seznam'] = Stran.objects.all()
        return context


def registracija(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Prosilci')
            user.groups.add(group)
            form.save()
            newuser = UporabnikProfil(uporabnik=user)
            newuser.save()

            return redirect('myapp:login')
    else:
        form = UserCreateForm()

    return render(request, 'myapp/registracija.html', {
        'form': form,
        'strani_seznam': Stran.objects.all(),
        'is_supervisor': request.user.groups.filter(name='Nadzorniki').exists(),
        'is_prosilec': request.user.groups.filter(name='Prosilci').exists()
    })


def aktiviraj(request):
    uporabniki = User.objects.filter(groups__name='Prosilci')

    return render(request, 'myapp/aktiviraj.html', {
        'stProsilcev': len(uporabniki),
        'stNavadnih': len(User.objects.filter(groups__name='Navadni')),
        'prosilci': uporabniki,
        'navadniUporabniki': User.objects.filter(groups__name='Navadni'),
        'nadzorniki': User.objects.filter(groups__name='Nadzorniki'),
        'is_supervisor': request.user.groups.filter(name='Nadzorniki').exists(),
        'is_prosilec': request.user.groups.filter(name='Prosilci').exists(),
        'strani_seznam': Stran.objects.all(),
    })


def potrdi(request, username):
    groupOld = Group.objects.get(name='Prosilci')
    groupNew = Group.objects.get(name='Navadni')
    user = User.objects.get(username=username)
    user.groups.remove(groupOld)
    user.groups.add(groupNew)
    user.save()

    return render(request, 'myapp/aktiviraj.html', {
        'stProsilcev': len(User.objects.filter(groups__name='Prosilci')),
        'stNavadnih': len(User.objects.filter(groups__name='Navadni')),
        'prosilci': User.objects.filter(groups__name='Prosilci'),
        'navadniUporabniki': User.objects.filter(groups__name='Navadni'),
        'nadzorniki': User.objects.filter(groups__name='Nadzorniki'),
        'is_supervisor': request.user.groups.filter(name='Nadzorniki').exists(),
        'is_prosilec': request.user.groups.filter(name='Prosilci').exists(),
        'strani_seznam': Stran.objects.all(),
    })

def spremeni(request, username):
    groupOld = Group.objects.get(name='Navadni')
    groupNew = Group.objects.get(name='Nadzorniki')
    user = User.objects.get(username=username)
    user.groups.remove(groupOld)
    user.groups.add(groupNew)
    user.save()

    return render(request, 'myapp/aktiviraj.html', {
        'stProsilcev': len(User.objects.filter(groups__name='Prosilci')),
        'stNavadnih': len(User.objects.filter(groups__name='Navadni')),
        'prosilci': User.objects.filter(groups__name='Prosilci'),
        'nadzorniki': User.objects.filter(groups__name='Nadzorniki'),
        'navadniUporabniki': User.objects.filter(groups__name='Navadni'),
        'is_supervisor': request.user.groups.filter(name='Nadzorniki').exists(),
        'is_prosilec': request.user.groups.filter(name='Prosilci').exists(),
        'strani_seznam': Stran.objects.all(),
    })