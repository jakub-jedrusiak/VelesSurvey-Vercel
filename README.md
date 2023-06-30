# VelesSurvey for Vercel

This is a template repository with a purpuse of making self-hosting [Veles](https://github.com/jakub-jedrusiak/VelesResearch) surveys easier. It includes a Django app that can be quickly deployed on Vercel. It can then be mapped to a subdomain like `surveys.uwr.edu.pl` or used directly. By default, this app uses MongoDB as its data storage. Some configuration is needed.

## Installation

1. On GitHub, click „Use this template” and create a new repository.

2. Go to [Vercel](https://vercel.com/) and create a new project. Link it to your newly created GitHub repo.

3. Don't change the default deployment settings but do click on `Enviroment variables`. Add a new variable named `SECRET_KEY` with a value generated with [this website](https://djecrety.ir/) and confirm with "Add" button. If you plan to use a custom domain, you can also add a `DOMAIN_NAME` variable with a value like `.uwr.edu.pl` to match all subdomains of `uwr.edu.pl`. Don't worry, if you don't know yet. You can always add it later. You can read more about custom domains [here](https://vercel.com/docs/concepts/projects/domains/add-a-domain).

![](https://github.com/jakub-jedrusiak/VelesDocs/blob/main/figs/getting_started/config_vercel.png)

4. When the building process ends, you can visit your page. It's just a white screen with a moving Veles logo. By design, there's no survey list on the main page. It helps keeping everything confidential.

5. Not only we need a place to collect our responses, but also somewhere to store them. For this purpuse we'll use MongoDB and its free 512 MB of space. My rough calculations say it will allow us to collect around 1 600 000 responses before the space runs out. I wish everyone this kind of probe sizes. Go to [MongoDB](https://www.mongodb.com/), create a free account and then a free cluster.

6. Now we need do connect Vercel and MongoDB. You can do it on [this website](https://vercel.com/integrations/mongodbatlas). Click "Add integration" and go with the forms.

7. That's it. Test your application by going to `/tea_survey` in your Vercel app (e.g. `https://tea-research-project.vercel.app/tea_survey/`). You should see a survey with a series of questions about tea. When you complete it, you should see a new response in your database.

## Using

When you create a survey with Veles, you get a folder with a series of files. The most important one is `main.js` from `build` subfolder. To add it to your site, you need to create a new subfolder in the `surveys` folder in your repository. The easiest way to do it it through [GitHub Desktop](https://desktop.github.com/). Use it to download (or "clone") your repository and create a new folder inside the `surveys` folder. The name of that folder will become a link to your survey, e.g. if you name it `black_tea_study`, the link will be something like `https://tea-research-project.vercel.app/black_tea_study`. Then put your `main.js` in your newly created folder. **Do not rename it.** Then use GitHub Desktop to upload (or "push") your changes. After a minute or so, your survey should be available.

To read and save your data you can use web desktop on [mongodb.com](https://www.mongodb.com/) or use a special program called [MongoDB Compass](https://www.mongodb.com/products/compass). After any responses are recieved (even for the tea survey), a new database called `VelesResponses` is created. Every survey gets its own folder (or "collection"). From there you can easily export your data to .csv or .json.
