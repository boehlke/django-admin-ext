
from django.contrib import admin

from djadmin_ext.helpers import BaseAjaxModelAdmin
from djadmin_ext.admin_forms import BaseAjaxModelForm
from sample import models

class MealAdminForm(BaseAjaxModelForm):
    ajax_change_fields = ["food_type", "main_ingredient"]

    @property
    def dynamic_fields(self):
        selected_food_type = self.data.get('food_type') or self.initial.get('food_type')
        if not selected_food_type:
            return {}

        food_type = models.FoodType.objects.get(pk=selected_food_type)

        selected_ingredient = self.get_selected_value('main_ingredient')

        if selected_ingredient:
            selected_ingredient = int(selected_ingredient)

        fields = {}

        ingredients = models.Ingredient.objects.filter(food_type=food_type)
        fields['main_ingredient'] = self.create_field_and_assign_initial_value(ingredients, selected_ingredient)

        if fields['main_ingredient'].initial:
            details = models.IngredientDetails.objects.filter(ingredient=selected_ingredient)

            if selected_ingredient and details:
                selected_ingredient_details = self.get_selected_value('ingredient_details')
                fields['ingredient_details'] = self.create_field_and_assign_initial_value(details,
                                                                                          selected_ingredient_details)

        return fields

    class Meta(object):
        fields = ['food_type']
        model = models.Meal

class MealAdmin(BaseAjaxModelAdmin):
    form = MealAdminForm

admin.site.register(models.FoodType)
admin.site.register(models.Ingredient)
admin.site.register(models.IngredientDetails)
admin.site.register(models.Meal, MealAdmin)