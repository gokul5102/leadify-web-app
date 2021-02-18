from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from agents.mixins import OrganiserAndLoginRequiredMixin
# class based views
from .forms import LeadForm,LeadModelForm,CustomUserCreationForm,AssignAgentForm,LeadCategoryUpdateForm
# Create your views here.

#CRUD-Create,Read,Update,Delete+List
#mixins allows us to check if a user is logged in:if user is not logged in then redirects to login

from .models import Lead,Agent,Category

class SignupView(generic.CreateView):
    template_name= "registration/signup.html"
    form_class=CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name="leads/landing.html"

def landing_page(request):
    return render(request,'leads/landing.html')

class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name="leads/lead_list.html"
    context_object_name="leads" #By default name of context is object_list,so we can modify it by this line
    
    #Assigned querysets
    def get_queryset(self):
        user=self.request.user

        #Initial queryset of leads for entire organisation
        if user.is_organiser:
            queryset=Lead.objects.filter(organisation=user.profile,agent__isnull=False)
        else:
            queryset=queryset=Lead.objects.filter(organisation=user.agent.organisation,agent__isnull=False)
            #filter for the agent who is logged in
            queryset=queryset.filter(agent__user=user) #user within agent model
        return queryset


    #Unassigned querysets
    def get_context_data(self,**kwargs):
        context=super(LeadListView,self).get_context_data(**kwargs)# to get already existing context data from leadlist class
        user=self.request.user
        if user.is_organiser:
            queryset=Lead.objects.filter(organisation=user.profile,agent__isnull=True)
            context.update({
                "unassigned_leads":queryset
           })
        return context

def lead_list(request):
    leads=Lead.objects.all()
    context={
        "leads":leads
    }
    return render(request,'leads/lead_list.html',context)


class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    template_name="leads/lead_detail.html"
    context_object_name="lead" 

    def get_queryset(self):
        user=self.request.user

        #Initial queryset of leads for entire organisation
        if user.is_organiser:
            queryset=Lead.objects.filter(organisation=user.profile)
        else:
            queryset=queryset=Lead.objects.filter(organisation=user.agent.organisation)
            #filter for the agent who is logged in
            queryset=queryset.filter(agent__user=user) #user within agent model
        return queryset


def lead_detail(request,pk):
    lead=Lead.objects.get(id=pk)
    context={
        "lead":lead
    }
    return render(request,'leads/lead_detail.html',context)


class LeadCreateView(OrganiserAndLoginRequiredMixin,generic.CreateView):
    template_name="leads/lead_create.html"
    form_class=LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead_list") #lead_list is name of url

    def form_valid(self,form):
        lead=form.save(commit=False)
        lead.organisation=self.request.user.profile
        lead.save()
        #TODO send email
        send_mail(
            
            subject="A lead has been created.",
            message="Go to the site",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView,self).form_valid(form) #Continue with LeadCreateView after sending email


def lead_create(request):
    form=LeadModelForm()
    if(request.method=="POST"):
        form=LeadModelForm(request.POST)
        if form.is_valid():
            form.save() #for directly pushing the data into Lead model
            return redirect('/leads')
    context={
        "form":form
    }
    return render(request,'leads/lead_create.html',context)



class LeadUpdateView(OrganiserAndLoginRequiredMixin,generic.UpdateView):
    template_name="leads/lead_update.html"
    form_class=LeadModelForm
    def get_queryset(self):
        user=self.request.user
        #Initial queryset of leads for entire organisation
        #Already know that the user is an organisor
        return Lead.objects.filter(organisation=user.profile)
    
    def get_success_url(self):
        return reverse("leads:lead_list")


def lead_update(request,pk):
    lead=Lead.objects.get(id=pk)
    form =LeadModelForm(instance=lead) #for updating a particular instance of Lead model while saving
    if(request.method=="POST"):
        form=LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context={
        "form":form,
        "lead":lead
    }
    return render(request,'leads/lead_update.html',context)


class LeadDeleteView(OrganiserAndLoginRequiredMixin,generic.DeleteView):
    template_name="leads/lead_delete.html"

    def get_queryset(self):
        user=self.request.user
        #Initial queryset of leads for entire organisation
        #Already know that the user is an organisor
        return Lead.objects.filter(organisation=user.profile)
    
    def get_success_url(self):
        return reverse("leads:lead_list")


def lead_delete(request,pk):
    lead=Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')


class CategoryListView(LoginRequiredMixin,generic.ListView):
    template_name='leads/category_list.html'
    context_object_name='category_list'
    
    def get_context_data(self,**kwargs):
        context=super(CategoryListView,self).get_context_data(**kwargs)
        user=self.request.user

        if user.is_organiser:
            queryset=Lead.objects.filter(organisation=user.profile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)

        
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })

        return context

    def get_queryset(self):
        user=self.request.user

        #Initial queryset of leads for entire organisation
        if user.is_organiser:
            queryset=Category.objects.filter(organisation=user.profile)
        else:
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset

class CategoryDetailView(LoginRequiredMixin,generic.DetailView):
    template_name='leads/category_detail.html'
    context_object_name='category'
    
    # def get_context_data(self,**kwargs):  do this within the template
    #     context=super(CategoryDetailView,self).get_context_data(**kwargs)

    #     qs=Lead.objects.filter(category=self.get_object())
    #     (get_object() is a part of DetailView and it fetches the context object we are working 
    #     with(here category))

    #     leads=self.get_object().leads.all()
    #     (this filters out all the leads within this particular category.Lead ->Category(Many->One)
    #     This special syntax is allowed only because category is a fk in leads model.
    #     leads is related_name in lead model for Category)

        
    #     context.update({
    #         "leads":leads
    #     })

    #     return context

    def get_queryset(self):
        user=self.request.user

        #Initial queryset of leads for entire organisation
        if user.is_organiser:
            queryset=Category.objects.filter(organisation=user.profile)
        else:
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset




class AssignAgentView(OrganiserAndLoginRequiredMixin,generic.FormView):
    template_name="leads/assign_agent.html"
    form_class=AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs=super(AssignAgentView,self).get_form_kwargs(**kwargs)

        kwargs.update({
            "request":self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead_list")

    def form_valid(self,form):
        agent=form.cleaned_data["agent"]
        lead=Lead.objects.get(id=self.kwargs["pk"])
        lead.agent=agent
        lead.save()
        return super(AssignAgentView,self).form_valid(form)

class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name="leads/lead_category_update.html"
    form_class=LeadCategoryUpdateForm
    def get_queryset(self):
        user=self.request.user

        #Initial queryset of leads for entire organisation
        if user.is_organiser:
            queryset=Lead.objects.filter(organisation=user.profile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
         # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    
    def get_success_url(self):
        return reverse("leads:lead_detail", kwargs={"pk": self.get_object().id})
        #self.get_object() refers to a particular lead
        #kwargs helps in passing pk to url

#     def lead_update(request,pk):
#     lead=Lead.objects.get(id=pk)
#     form=LeadForm()
#     if(request.method=="POST"):
#         form=LeadForm(request.POST)
#         if form.is_valid():
#             first_name=form.cleaned_data['first_name']
#             last_name=form.cleaned_data['last_name']
#             age=form.cleaned_data['age']
#             lead.first_name=first_name,
#             lead.last_name=last_name,
#             lead.age=age,
#             return redirect('/leads')
#     context={
#         "form":form,
#         "lead":lead
#     }
#     return render(request,'leads/lead_update.html',context)


# def lead_create(request):
#     form=LeadForm()
#     if(request.method=="POST"):
#         form=LeadForm(request.POST)
    # if form.is_valid():
    #         first_name=form.cleaned_data['first_name']
    #         last_name=form.cleaned_data['last_name']
    #         age=form.cleaned_data['age']
    #         agent=Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
    #         return redirect('/leads')
    # context={
    #     "form":form
    # }
    # return render(request,'leads/lead_create.html',context)