from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.uploadedfile import InMemoryUploadedFile

from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView

from store.models import Pic
from store.forms import CreateForm

import short_url# I found it's useful
#print(short_url.encode_url(2))

"""
def pk2code(pk):
    code = "p"
    while(1):
        ch=pk%62
        print(pk)

        if (ch<10):
            code += chr(ch+ord('0'))
        elif (ch<36):
            ch -= 10
            code += chr(ch+ord('a'))
        else:
            ch -= 36
            code += chr(ch+ord('A'))

        pk//=62
        if (pk==0): break
    return code
"""

class PicListView(ListView):
    model = Pic
    template_name = "store/list.html"
    def get(self, request):
        search = request.GET.get('search')
        if search:
            img = Pic.objects.filter(code=search)
            print(img)
            if img.exists(): 
                return redirect(reverse_lazy('store:pic_detail', kwargs={'code': search}))
        return render(request, self.template_name)

class PicDetailView(TemplateView):
    model = Pic
    template_name = "store/detail.html"
    def get(self, request, code=None):
        print(Pic.objects.get(code=code))
        print(self.template_name)
        ctx = {'pic': Pic.objects.get(code=code)}
        return render(request, self.template_name, ctx)

class PicCreateView(CreateView):
    template = 'store/form.html'
    def get(self, request, pk=None) :
        tm_s = request.GET.get('d')
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        print(request.FILES.keys())

        pic = form.save()
        #print("OK", request.FILES["FILES"])
        pic.code = short_url.encode_url(pic.id)#pk2code(pic.id)
        pic.save()
        print(pic.code)
        return redirect(reverse_lazy('store:pic_detail', kwargs={'code': pic.code}))

def stream_file(request, pk) :
    pic = get_object_or_404(Pic, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response

