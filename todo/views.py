from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from todo.models import Task


class TaskView(CreateView):
    model = Task
    fields = "__all__"  # " " - with them django doesn't check automatically if exist
    template_name = 'to_do/todo.html'
    success_url = reverse_lazy('todo:todo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_list'] = Task.objects.filter(is_done=False, archive=False)
        return context
