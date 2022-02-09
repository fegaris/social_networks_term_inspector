# social_networks_term_inspector
Buscador común de términos en las distintas redes sociales


## Notas desarrollo
La libreria se encuentra en la carpeta **lib**
En esta carpeta tenemos un archivo main.py que sera el encargado de realizar las llamadas necesarias a todas las implementaciones
de la interfaz "social".
Estas implementaciones se encuentran en la carpeta **social_apis**

# Create the library
If you want to use the library you needs create and install first.

**Create**
Firs of all, you need the library `wheel`. You can install with `pip install wheel` command.

Download the repository and open your prompt in the project root folder.
Execute the next command to create "dist" folder with the library installer
`python setup.py bdist_wheel`

**Install**
When the command finish you are able to install the library with "pip".
Execute the next command replacing the .whl filename:
`pip install .\dist\social_networks_term_inspector_[insert version].whl --force-reinstall`

**Use**
Now you can import the library in your projects as a regular library using 


# How calculate the engagement

| Social Network   |      Formula      |
| ------------- | ------------- |
| YouTube |  (Likes + Favs + Shared + Comments) / Views|
| LinkedIn |    (Clicks + Likes + Comments) / Views   |
| Tik-Tok | (Likes + Comments + Shared) / Views |
| Twitter | (Mentions + ReTweets + likes) / Followers |
| Twitch | ???? |
| Instagram | (Likes + Comments) / Followers |



