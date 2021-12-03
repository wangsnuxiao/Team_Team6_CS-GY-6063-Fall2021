from django.urls import path
from . import views

app_name = "creation"

urlpatterns = [
    path("", views.daylist),
    path("<int:day_id>/detail", views.viewMap),
    path("<int:day_id>/edit", views.editPage),
    path("<int:day_id>/edit/searchpage", views.searchpage),
    path("<int:day_id>/edit/delete_dayvenue/<int:dayvenue_id>", views.delete_dayvenue),
    path("delete_day", views.deleteday),
    path("<int:day_id>/edit/<int:dv_id>/up", views.day_venue_up),
    path("<int:day_id>/edit/<int:dv_id>/down", views.day_venue_down),
    path("<int:day_id>/edit/categories", views.edit_categories_page),
    path("<int:day_id>/edit/categories/add/<int:daycat_id>", views.add_daycategory),
    path(
        "<int:day_id>/edit/categories/remove/<int:daycat_id>", views.remove_daycategory
    ),
]
