from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from todo.models import Task


class TaskView(CreateView):
    model = Task
    fields = ['details', 'owner']  # " " - with them django doesn't check automatically if exist
    template_name = 'to_do/todo.html'
    success_url = reverse_lazy('todo:todo')

    def get_context_data(self, **kwargs):
        filter_ = self.kwargs.get('filter', None)
        context = super().get_context_data(**kwargs)
        if filter_ is None or filter_ == 'ongoing':
            context['task_list'] = Task.objects.filter(is_done=False, archive=False)
        elif filter_ == 'all':
            context['task_list'] = Task.objects.filter(archive=False)
        elif filter_ == 'done':
            context['task_list'] = Task.objects.filter(is_done=True, archive=False)

        return context


class DeleteTaskView(View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.archive = True
        task.save()
        return HttpResponseRedirect(reverse('todo:todo'))


class DoneTaskView(View):
    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.is_done = True
        task.save()
        return HttpResponseRedirect(reverse('todo:todo'))
