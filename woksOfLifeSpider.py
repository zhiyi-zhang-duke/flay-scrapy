import scrapy

#Usage: scrapy runspider woksOfLifeSpider.py -o wol_recipes.json > woksoflife_out.log 2>&1
class WoksOfLifeSpider(scrapy.Spider):
	name = 'recipes'
	start_urls = [
		'https://thewoksoflife.com/chinese-preserved-greens/',
	]

	def parse(self, response):
		print("Recipe name:")
		recipe = response.css('.wprm-recipe-name::text').get()
		print(recipe)

		print("Time to make:")
		raw_time = response.css('.wprm-recipe-times-container *::text').getall()
		print(' '.join(text.strip() for text in raw_time))

		print("Tags:")
		raw_tags = response.css('.wprm-recipe-tags-container *::text').getall()
		tags = []
		for tag in raw_tags:
			if ":" not in tag:
				tags.append(tag)
		print(tags)

		print("Nutrition:")
		print(response.css('.wprm-nutrition-label-text-nutrition-label *::text, .wprm-nutrition-label-text-nutrition-value *::text').getall())

		print("Steps:")
		steps = response.css('.wprm-recipe-instruction-group *::text').getall()
		print(steps)		

		print("Number of Steps:")
		print(len(steps))

		print("Recipe description:")
		print(response.css('.wprm-recipe-summary *::text').get())

		print("Ingredients:")
		ingredients = response.css('.wprm-recipe-ingredients-container *::text').getall()
		print(ingredients)

		print("Number of Ingredients:")
		print(len(ingredients))

		yield set(
			recipe=recipe,
			tags=tags
		)


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



