import scrapy
from recipeItem import RecipeItem
import json


#Usage: scrapy runspider woksOfLifeSpider.py -o wol_recipes.json > woksoflife_out.log 2>&1
class WoksOfLifeSpider(scrapy.Spider):
	name = 'recipes'
	start_urls = [
		'https://thewoksoflife.com/chinese-preserved-greens/',
	]

	def parse(self, response):
		#Create scrapy item
		item = RecipeItem()

		#Use embedded scema graph for data
		json_data = json.loads(response.css('.yoast-schema-graph::text').get())
		recipe_data = json_data["@graph"][-1]
		author_data = json_data["@graph"][6]
		submission_data = json_data["@graph"][5]

		#Recipe name
		item["recipeName"] = recipe_data["name"]

		#Time to make
		#This assumes the
		formattedTime = "Preptime: "
		prepTimeRaw = int(recipe_data["prepTime"][2:-1])
		prepTimeDay = prepTimeRaw // (24 * 60)
		if prepTimeDay > 0:
			formattedTime+=(str(prepTimeDay) + " days")
			prepTimeRaw = prepTimeRaw % (24 * 60)
		prepTimeHour = prepTimeRaw // 60
		if prepTimeHour > 0:
			formattedTime+=(" " + str(prepTimeHour) + " hours")
			prepTimeRaw = prepTimeRaw % 60
		if prepTimeRaw > 0:
			formattedTime+=(" " + str(prepTimeRaw) + " minutes")		

		totalTimeRaw = int(recipe_data["totalTime"][2:-1])
		totalTimeDay = totalTimeRaw // (24 * 60)
		if totalTimeDay > 0:
			formattedTime+=(str(totalTimeDay) + " days")
			totalTimeRaw = totalTimeRaw % (24 * 60)
		totalTimeHour = totalTimeRaw // 60
		if totalTimeHour > 0:
			formattedTime+=(" " + str(totalTimeHour) + " hours")
			totalTimeRaw = totalTimeRaw % 60
		if totalTimeRaw > 0:
			formattedTime+=(" " + str(totalTimeRaw) + " minutes")	

		item['minutesToMake']= formattedTime

		#Tags
		item['tags'] = recipe_data["recipeCuisine"][0]

		#Nutrition
		item['nutrition'] = recipe_data["nutrition"]

		#Steps:
		stepsRaw = recipe_data["recipeInstructions"]
		stepsFormatted = []
		for raw in stepsRaw:
			stepsFormatted.append(raw["text"])
		item['steps'] = stepsFormatted

		#Number of Steps
		item['n_steps'] = len(stepsFormatted)

		#Recipe description
		item['description'] = recipe_data["description"]

		#Ingredients
		ingredients = recipe_data["recipeIngredient"]
		item['ingredients'] = ingredients

		#Number of Ingredients
		item['n_ingredients'] = len(ingredients)

		item['contributor'] = author_data["name"]
		item['dateSubmitted'] = submission_data["datePublished"]

		yield item


	def oldParse(self, response):
		item = RecipeItem()

		#Recipe name
		recipe = response.css('.wprm-recipe-name::text').get()
		item["recipeName"] = recipe

		#Time to make
		raw_time = response.css('.wprm-recipe-times-container *::text').getall()
		item['minutesToMake']= ' '.join(text.strip() for text in raw_time)

		#"Tags:")
		raw_tags = response.css('.wprm-recipe-tags-container *::text').getall()
		tags = []
		for tag in raw_tags:
			if ":" not in tag:
				tags.append(tag)
		item['tags'] = tags

		#"Nutrition
		item['nutrition'] = response.css('.wprm-nutrition-label-text-nutrition-label *::text, .wprm-nutrition-label-text-nutrition-value *::text').getall()

		#Steps:
		steps = response.css('.wprm-recipe-instruction-group *::text').getall()
		item['steps'] = steps

		#Number of Steps
		item['n_steps'] = len(steps)

		#Recipe description
		item['description'] = response.css('.wprm-recipe-summary *::text').get()

		#Ingredients
		ingredients = response.css('.wprm-recipe-ingredients-container *::text').getall()
		item['ingredients'] = ingredients

		#Number of Ingredients
		item['n_ingredients'] = len(ingredients)

		item['contributor'] = "N/A"
		item['dateSubmitted'] = "N/A"

		yield item


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
# contributor_id					
# date submitted

#Current output
# Recipe name:
# Chinese Preserved Greens
# Time to make:
# Prep Time 4  d Total Time 4  d
# Tags:
# ['Vegetables', 'Chinese', 'Chinese Preserved Greens']
# Nutrition:
# ['Calories: ', '37', 'Carbohydrates: ', '7', 'Protein: ', '3', 'Fat: ', '1', 'Saturated Fat: ', '1', 'Sodium: ', '1105', 'Potassium: ', '368', 'Vitamin A: ', '7493', 'Vitamin C: ', '90', 'Calcium: ', '113', 'Iron: ', '1']
# Steps:
# ['Make sure all containers, work surfaces, your knife, and your hands are thoroughly cleaned and free of any dirt, grease, or grime. ', 'Let them air dry completely for 12 hours. If you have loose stalks and leaves like I did, you can bundle them together with kitchen string or rubber bands, and hang them on a line of clean twine to dry. ', 'Once all the leaves are dried (free of surface water, not dehydrated) and slightly wilted, chop them to your desired size—I did small slivers. You can also cut them into larger chunks or leave them whole.', 'In a large bowl, sprinkle salt onto every layer of greens. Knead the vegetables with clean hands to work the salt in, until they are well coated. Transfer everything to a clean container with a cover. Marinate in the refrigerator for at least 3 days. After three days, they are ready to be used! ']
# Number of Steps:
# 4
# Recipe description:
# These Chinese Preserved Greens can be made with any robust leafy green vegetable, like tender kale, mustard greens, or radish greens. All you need is salt!
# Ingredients:
# ['Ingredients', '2.7', ' ', 'kg', ' ', 'fresh kale, mustard greens, or radish greens', ' ', '(6 pounds)', '100', ' ', 'g', ' ', 'sea salt', ' ', '(about 1/3 cup)']
# Number of Ingredients:
# 15



