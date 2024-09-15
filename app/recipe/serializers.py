"""
Serializers for recipe API
"""

from rest_framework import serializers

from core.models import Recipe, Tag, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients"""

    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""

    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
                    "id",
                    "title",
                    "time_minutes",
                    "price",
                    "link",
                    "tags",
                    "ingredients"
                ]
        read_only_fileds = ["id"]

    def _get_or_create_objects(self, objects, dest_location, obj_class):
        """Handle getting or creating objects as needed"""
        auth_user = self.context["request"].user

        for object_data in objects:
            obtained_obj, _ = obj_class.objects.get_or_create(
                user=auth_user,
                **object_data,
            )
            dest_location.add(obtained_obj)

    def create(self, validated_data):
        """Create a recipe"""
        tags = validated_data.pop("tags", [])
        ingredients = validated_data.pop("ingredients", [])

        recipe = Recipe.objects.create(**validated_data)

        self._get_or_create_objects(tags, recipe.tags, Tag)
        self._get_or_create_objects(ingredients,
                                    recipe.ingredients,
                                    Ingredient)

        return recipe

    def update(self, instance, validated_data):
        """Update a recipe"""
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredients", None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_objects(tags, instance.tags, Tag)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_objects(ingredients,
                                        instance.ingredients,
                                        Ingredient)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
