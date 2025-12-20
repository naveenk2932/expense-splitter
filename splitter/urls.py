from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.group_list, name='group_list'),
    path('group/add/', views.group_add, name='group_add'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),

    path('member/add/<int:group_id>/', views.member_add, name='member_add'),
    path('member/edit/<int:member_id>/', views.member_edit, name='member_edit'),
    path('member/delete/<int:member_id>/', views.member_delete, name='member_delete'),

    path('expense/add/<int:group_id>/', views.expense_add, name='expense_add'),
    path('expense/edit/<int:expense_id>/', views.expense_edit, name='expense_edit'),
    path('expense/delete/<int:expense_id>/', views.expense_delete, name='expense_delete'),
]
