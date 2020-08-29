# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#Reference of things to pull
# Recipe name
# Minutes to make
# tags
# nutrition
# n_steps
# steps
# description
# ingredients
# n_ingredients

from scrapy.item import Item, Field

class RecipeItem(Item):
    recipeName = Field()
    minutesToMake = Field()
    tags = Field()
    nutrition = Field()
    n_steps = Field()
    steps = Field()
    description = Field()
    ingredients = Field()
    n_ingredients = Field()
    contributor = Field()
    dateSubmitted = Field()
