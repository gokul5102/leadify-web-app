from django.shortcuts import render,reverse
import random
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganiserAndLoginRequiredMixin
from django.core.mail import send_mail
# Create your views here.

class AgentListView(OrganiserAndLoginRequiredMixin,generic.ListView):
    template_name='agents/agent_list.html'

    def get_queryset(self):
        organisation=self.request.user.profile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganiserAndLoginRequiredMixin,generic.CreateView):
    template_name="agents/agent_create.html"
    form_class=AgentModelForm
    
    def get_success_url(self):
        return reverse("agents:agent_list") 

    def form_valid(self,form):
        user=form.save(commit=False)
        user.is_agent=True
        user.is_organiser=False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.profile,
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You are added as an agent on DJCRM.Please login to start working.",
            from_email="admin@test.com",
            recipient_list=[user.email],
        )
        # agent.organisation=self.request.user.profile
        # agent.save()
        return super(AgentCreateView,self).form_valid(form)


class AgentDetailView(OrganiserAndLoginRequiredMixin,generic.DetailView):
    template_name="agents/agent_detail.html"
    context_object_name="agent"
    
    def get_queryset(self):
        return Agent.objects.all()

class AgentUpdateView(OrganiserAndLoginRequiredMixin,generic.UpdateView):
    template_name="agents/agent_update.html"
    form_class=AgentModelForm
    
    def get_success_url(self):
        return reverse("agents:agent_list") 

    def get_queryset(self):
        organisation=self.request.user.profile
        return Agent.objects.filter(organisation=organisation)

class AgentDeleteView(OrganiserAndLoginRequiredMixin,generic.DeleteView):
    template_name="agents/agent_delete.html"
    context_object_name="agent"

    def get_success_url(self):
        return reverse("agents:agent_list") 
    
    def get_queryset(self):
        organisation=self.request.user.profile
        return Agent.objects.filter(organisation=organisation)


