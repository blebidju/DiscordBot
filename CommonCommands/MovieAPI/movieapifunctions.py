import discord
import requests
import datetime
import random

API_TOKEN_TMDB = "Redacted"
API_TOKEN_OMDB = "Redacted"

def find_options(message, options):
    # first index of the first character of the option
    first = message.find('[') + 1
    # index of the last character of the title
    last = message.find(']')
    if (first == 0 or last == -1):
        return options
    options.append(message[first:last])
    message = message[last+1:]
    return find_options(message, options) 


async def mediaSearch(ctx, bot):
    message = ctx.message.clean_content

    options = find_options(message, [])
    
    returnedMovieQuery = await mediaSearchQuery(options[0])
    
    movieQueryIndex = 0
    if(len(options) == 2):
        movieQueryIndex = int(options[1])
        
    movieQueryList = returnedMovieQuery.json()["results"]
    
    if(len(movieQueryList) != 0):
        movieQueryResult = movieQueryList[movieQueryIndex]
        
        if(movieQueryResult["media_type"] == "movie"):
            await getMovieInfo(ctx, str(movieQueryResult["id"]), str(movieQueryResult["poster_path"]))
        elif(movieQueryResult["media_type"] == "tv"):
            await getTVInfo(ctx, movieQueryResult)
        elif(movieQueryResult["media_type"] == "person"):
            await getPersonInfo(ctx, movieQueryResult)
        else:
            await botError(ctx, "Bot could not find the requested media...")
            
    else:
        await botError(ctx, "Bot could not find the requested media...")

async def findMediaID(ctx, bot):
    message = ctx.message.clean_content

    options = find_options(message, [])
    
    returnedMovieQuery = await mediaSearchQuery(options[0])
    movieQueryList = returnedMovieQuery.json()["results"]
    
    if(len(movieQueryList) != 0):
        
        embed=discord.Embed(color=discord.Color(11812188))
        embed.set_author(name="Bot Media Index List", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        
        index = 0
        for x in movieQueryList:
            if(x["media_type"] == "movie"):
                embed.add_field(name="**Movie** Index "+str(index), value="\nTitle: "+ifNull(str(x["title"]))+" Release Date: "+ifNull(str(x["release_date"])), inline=False)
            elif(x["media_type"] == "tv"):
                if 'first_air_date' in x:
                    embed.add_field(name="**TV** Index "+str(index), value="\nTitle: "+ifNull(str(x["name"]))+" First Air Date: "+ifNull(str(x["first_air_date"])), inline=False)
                else:
                    embed.add_field(name="**TV** Index "+str(index), value="\nTitle: "+ifNull(str(x["name"])), inline=False)
            elif(x["media_type"] == "person"):
                embed.add_field(name="**Person** Index "+str(index), value="\nName: "+ifNull(str(x["name"])), inline=False)
                
            index += 1
                
        await ctx.message.channel.send(embed=embed)  
    else:
        await botError(ctx, "Bot could not find the requested media...")
        
async def mediaSearchQuery(query):
    headerData = {
        'Content-Type': 'application/json'
    }
    try:
        request = requests.get('https://api.themoviedb.org/3/search/multi?api_key='+API_TOKEN_TMDB+'&query='+query+'', headers = headerData)
        print(request.text)
        return(request)
    
    except KeyError:
        await botError(ctx, "Bot ran into an issue...")
        return "Something wrong with movie function"
    
async def getMovieInfo(ctx, id, image):
    headerData = {
        'Content-Type': 'application/json'
    }
    
    try:
        request = requests.get('https://api.themoviedb.org/3/movie/'+id+'?api_key='+API_TOKEN_TMDB, headers = headerData)
        TMDBinfo = request.json()
        print(str(TMDBinfo))
              
        if(TMDBinfo["imdb_id"] is None):
            
            title = ifNull(str(TMDBinfo["title"]))
            
            year = ifNull(str(TMDBinfo["release_date"]))
            runtime = ifNull(str(TMDBinfo["runtime"]))
            
            if runtime != "N/A":
                runtime = runtime + ' minutes'
            
            genre = ''
            for x in TMDBinfo["genres"]:
                genre = genre + x["name"] + ', '
            
            genre = ifNull(genre)
            if genre != "N/A":
                genre = genre[0:len(genre)-2]
            
            plot = "N/A"
            
            if(ifNull(str(TMDBinfo["overview"])) != "N/A"):
                plotString = str(TMDBinfo["overview"])
                
                plotSubstringEnding = len(plotString)
                plotSubstringValue = plotString[0:plotSubstringEnding]
                
                if(len(plotString) > 1000):
                    plotSubstringEnding = 1000
                    plotSubstringValue = plotString[0:plotSubstringEnding]+"..."
                
                print(plotSubstringValue)
                print(plotSubstringEnding)
                print(len(plotString))
                
                plot = plotSubstringValue
                
            embed=discord.Embed(color=discord.Color(11812188))
            embed.set_author(name="Bot Movie Info", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
            embed.add_field(name="**Title**", value=title, inline=False)
            embed.add_field(name="**Date**", value=year, inline=True)
            embed.add_field(name="**Runtime**", value=runtime, inline=True)
            embed.add_field(name="**Genre**", value=genre, inline=True)
            embed.add_field(name="**Plot**", value=plot, inline=False)
            
            if(ifNull(image) != "N/A"):
                imageLink = "https://image.tmdb.org/t/p/original"+image
                embed.set_image(url=imageLink)

            await ctx.message.channel.send("Bot couldn't find the imdb link so here is only some of the data")
            await ctx.message.channel.send(embed=embed)
        else:
            await getMovieInfoOMDB(ctx, str(TMDBinfo["imdb_id"]), image)
    
    except KeyError:
        await botError(ctx, "Bot ran into an issue...")
        return "Something wrong with movie function"
    
async def getMovieInfoOMDB(ctx, id, image):   
    headerData = {
        'Content-Type': 'application/json'
    }
    
    request = requests.get('http://www.omdbapi.com/?i='+id+'&plot=full&apikey='+API_TOKEN_OMDB, headers = headerData)
    OMDBinfo = request.json()
    print(str(OMDBinfo))
    
    title = ifNull(str(OMDBinfo["Title"]))
    year = ifNull(str(OMDBinfo["Year"]))
    runtime = ifNull(str(OMDBinfo["Runtime"]))
    genre = ifNull(str(OMDBinfo["Genre"]))
    
    imdb = "N/A"
    rt = "N/A"
    metacritic = "N/A"
    
    for x in OMDBinfo["Ratings"]:
        if(str(x["Source"]) == "Internet Movie Database"):
            imdb = ifNull(str(x["Value"]))
        elif(str(x["Source"]) == "Rotten Tomatoes"):
            rt = ifNull(str(x["Value"]))
        elif(str(x["Source"]) == "Metacritic"):
            metacritic = ifNull(str(x["Value"]))
    
    plot = "N/A"
    
    if(ifNull(str(OMDBinfo["Plot"])) != "N/A"):
        plotString = str(OMDBinfo["Plot"])
        
        plotSubstringEnding = len(plotString)
        plotSubstringValue = plotString[0:plotSubstringEnding]
        
        if(len(plotString) > 1000):
            plotSubstringEnding = 1000
            plotSubstringValue = plotString[0:plotSubstringEnding]+"..."
        
        print(plotSubstringValue)
        print(plotSubstringEnding)
        print(len(plotString))
        
        plot = plotSubstringValue
        
    director = ifNull(str(OMDBinfo["Director"]))
    writers = ifNull(str(OMDBinfo["Writer"]))
    actors = ifNull(str(OMDBinfo["Actors"]))
    awards = ifNull(str(OMDBinfo["Awards"]))
        
    embed=discord.Embed(color=discord.Color(11812188))
    embed.set_author(name="Bot Movie Info", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
    embed.add_field(name="**Title**", value=title, inline=False)
    embed.add_field(name="**Year**", value=year, inline=True)
    embed.add_field(name="**Runtime**", value=runtime, inline=True)
    embed.add_field(name="**Genre**", value=genre, inline=True)
    embed.add_field(name="\n<:imdb:933914550640717824> **IMBD**", value=imdb, inline=True)
    embed.add_field(name="<:rottentomatoes:933914550993043536> **Rotten Tomatoes**", value=rt, inline=True)
    embed.add_field(name="<:metacritic:933914551475372043> **Metacritic**", value=metacritic, inline=True)
    embed.add_field(name="**Plot**", value=plot, inline=False)
    embed.add_field(name="**Directors**", value=director, inline=False)
    embed.add_field(name="**Writers**", value=writers, inline=False)
    embed.add_field(name="**Actors/Actresses**", value=actors, inline=False)
    embed.add_field(name="**Awards**", value=awards, inline=False)
    
    if(ifNull(image) != "N/A"):
        imageLink = "https://image.tmdb.org/t/p/original"+image
        embed.set_image(url=imageLink)

    await ctx.message.channel.send(embed=embed)
    
async def getMovieInfoRandom(ctx):
    headerData = {
        'Content-Type': 'application/json'
    }
    
    try:
        randomPage = random.randint(1, 500)
        request = requests.get('https://api.themoviedb.org/3/discover/movie?api_key='+API_TOKEN_TMDB+'&page='+str(randomPage)+'&include_adult=false', headers = headerData)
        
        randomResult = random.randint(0, len(request.json()["results"])-1)
        TMDBinfo = request.json()["results"][randomResult]
        
        print(randomPage)
        print(randomResult)
        print(str(TMDBinfo))
        print(request.json()["results"])
              
        if(TMDBinfo["id"] is None):
            await botError(ctx, "Bot ran into an issue...")
        else:
            await getMovieInfo(ctx, str(TMDBinfo["id"]), str(TMDBinfo["poster_path"]))
    
    except KeyError:
        await botError(ctx, "Bot ran into an issue...")
        return "Something wrong with movie function"
    
async def getTVInfo(ctx, tvResult):
    embed = ""
    if(ifNull(str(tvResult["overview"])) != "N/A"):
        overviewString = str(tvResult["overview"])
        
        overviewSubstringEnding = len(overviewString)
        overviewSubstringValue = overviewString[0:overviewSubstringEnding]
        
        if(len(overviewString) > 2000):
            overviewSubstringEnding = 2000
            overviewSubstringValue = overviewString[0:overviewSubstringEnding]+"..."
        
        print(overviewSubstringValue)
        print(overviewSubstringEnding)
        print(len(overviewString))
        
        embed=discord.Embed(color=discord.Color(11812188), title=ifNull(str(tvResult["name"])), description=overviewSubstringValue)

    else:
        embed=discord.Embed(color=discord.Color(11812188), title=ifNull(str(tvResult["name"])))
        
    embed.set_author(name="Bot TV Info", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
    
    dateString = "N/A"
    
    if 'first_air_date' in tvResult:        
        if(ifNull(str(tvResult["first_air_date"])) != "N/A"):
            x = str(tvResult["first_air_date"]).split('-')
            dateTimeObject = datetime.datetime(int(x[0]), int(x[1]), int(x[2]))
            dateString = dateTimeObject.strftime("%B")+" "+dateTimeObject.strftime("%d")+", "+dateTimeObject.strftime("%Y")

    embed.add_field(name="**First Air Date**", value=dateString, inline=False)
    
    if(ifNull(str(tvResult["poster_path"])) == "N/A"):
        print("no poster path")
    else:
        embed.set_image(url='https://image.tmdb.org/t/p/w300'+str(tvResult["poster_path"])+'')
        
    await ctx.message.channel.send(embed=embed)
    
async def getPersonInfo(ctx, personInfo):
    headerData = {
        'Content-Type': 'application/json'
    }
    
    try:
        request = requests.get('https://api.themoviedb.org/3/person/'+str(personInfo["id"])+'?api_key='+API_TOKEN_TMDB, headers = headerData)
        personInfo2 = request.json()
        print(str(personInfo2))
        embed=""
        
        if(ifNull(str(personInfo2["biography"])) != "N/A"):
            biographyString = str(personInfo2["biography"])
            
            biographySubstringEnding = len(biographyString)
            biographySubstringValue = biographyString[0:biographySubstringEnding]
            
            if(len(biographyString) > 2000):
                biographySubstringEnding = 2000
                biographySubstringValue = biographyString[0:biographySubstringEnding]+"..."
            
            print(biographySubstringValue)
            print(biographySubstringEnding)
            print(len(biographyString))
            
            embed=discord.Embed(color=discord.Color(11812188), title=ifNull(str(personInfo["name"])), description=biographySubstringValue)
            
        else:
            embed=discord.Embed(color=discord.Color(11812188), title=ifNull(str(personInfo["name"])))
            
        
        embed.set_author(name="Bot Actor/Actress Info", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
        embed.add_field(name="**Place of Birth**", value=ifNull(str(personInfo2["place_of_birth"])), inline=False)
        embed.add_field(name="**Department**", value=ifNull(str(personInfo["known_for_department"])), inline=False)

        if(len(personInfo["known_for"]) != 0):
            moviesList = ''
            if("title" in personInfo["known_for"][0]):
                moviesList = str(personInfo["known_for"][0]["title"])
            elif("name" in personInfo["known_for"][0]):
                moviesList = str(personInfo["known_for"][0]["name"])

            i = 1;
            print(personInfo["known_for"])
            while i < len(personInfo["known_for"]):
                if("title" in personInfo["known_for"][i]):
                    moviesList = moviesList + ', ' +  ifNull(str(personInfo["known_for"][i]["title"]))
                elif("name" in personInfo["known_for"][i]):
                    moviesList = moviesList + ', ' +  ifNull(str(personInfo["known_for"][i]["name"]))
                i+=1;
            embed.add_field(name="**Known For**", value=moviesList, inline=False)
            
        if(ifNull(str(personInfo2["imdb_id"])) != "N/A"):
            embed.add_field(name="**IMBD Page**", value="https://www.imdb.com/name/"+str(personInfo2["imdb_id"]), inline=False)

        if(ifNull(str(personInfo["profile_path"])) != "N/A"):
            embed.set_image(url='https://image.tmdb.org/t/p/w300'+str(personInfo["profile_path"])+'')
        
        await ctx.message.channel.send(embed=embed)
    
    except KeyError:
        await botError(ctx, "Bot ran into an issue...")
        return "Something wrong with movie function"
    
async def getCredits(ctx):
    headerData = {
        'Content-Type': 'application/json'
    }
    
    message = ctx.message.clean_content

    options = find_options(message, [])
    
    returnedMovieQuery = await mediaSearchQuery(options[0])
    movieQueryList = returnedMovieQuery.json()["results"]
    
    if(len(movieQueryList) != 0):
        index = 0
        foundMovie = False
        
        if(len(options) == 2):
            foundMovie = True
            index = int(options[1])
        else:
            while(index < len(movieQueryList) and foundMovie == False):
                if(movieQueryList[index]["media_type"] == "movie"):
                    foundMovie = True
                else:
                    index += 1
                
        if(foundMovie == False):
            await botError(ctx, "Bot could not find the requested media...")
        else:
            try:
                request = requests.get('https://api.themoviedb.org/3/movie/'+str(movieQueryList[index]["id"])+'?api_key='+API_TOKEN_TMDB, headers = headerData)
                TMDBinfo = request.json()
                print(str(TMDBinfo))
                      
                if(TMDBinfo["imdb_id"] is None):
                    try:
                        requestCrew = requests.get('https://api.themoviedb.org/3/movie/'+str(movieQueryList[index]["id"])+'/credits?api_key='+API_TOKEN_TMDB, headers = headerData)
                        Crewinfo = requestCrew.json()
                        print(str(Crewinfo))
                        
                        CrewList = {}
                        for x in Crewinfo["cast"]:
                            if(str(x["known_for_department"]) in CrewList):
                                if(len(CrewList[str(x["known_for_department"])]) > 900):
                                    y=1
                                else:
                                    if(str(x["known_for_department"]) == "Acting"):
                                        CrewList[str(x["known_for_department"])] = CrewList[ifNull(str(x["known_for_department"]))] +' '+ ifNull(str(x["name"])) +' as '+ ifNull(str(x["character"])) +','
                                    else:
                                        CrewList[str(x["known_for_department"])] = CrewList[ifNull(str(x["known_for_department"]))] +' '+ ifNull(str(x["name"])) +','
                            else:
                                if(str(x["known_for_department"]) == "Acting"):
                                    CrewList[ifNull(str(x["known_for_department"]))] = ifNull(str(x["name"])) +' as '+ ifNull(str(x["character"])) +','
                                else:
                                    CrewList[ifNull(str(x["known_for_department"]))] = ifNull(str(x["name"])) +','
                                
                        
                        title = ifNull(str(TMDBinfo["title"]))

                        
                        embed=discord.Embed(color=discord.Color(11812188))
                        embed.set_author(name="Bot Crew Info", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
                        embed.add_field(name="**Title**", value=title, inline=False)
                        
                        for key, value in CrewList.items():
                            print(key)
                            print(value[0:len(value)-1])
                            embed.add_field(name="**"+key+"**", value=value[0:len(value)-1], inline=False)
                            
                        if(ifNull(str(movieQueryList[index]["poster_path"])) != "N/A"):
                            imageLink = "https://image.tmdb.org/t/p/original"+str(movieQueryList[index]["poster_path"])
                            embed.set_image(url=imageLink)
                            
                        await ctx.message.channel.send(embed=embed)
                            
                    except KeyError:
                        await botError(ctx, "Bot could not find the requested media...")
                else:
                    try:
                        request = requests.get('http://www.omdbapi.com/?i='+str(TMDBinfo["imdb_id"])+'&plot=full&apikey='+API_TOKEN_OMDB, headers = headerData)
                        requestCrew = requests.get('https://api.themoviedb.org/3/movie/'+str(movieQueryList[index]["id"])+'/credits?api_key='+API_TOKEN_TMDB, headers = headerData)
                        OMDBinfo = request.json()
                        Crewinfo = requestCrew.json()
                        print(str(OMDBinfo))
                        print(str(Crewinfo))
                        
                        CrewList = {}
                        for x in Crewinfo["cast"]:
                            if(str(x["known_for_department"]) in CrewList):
                                if(len(CrewList[str(x["known_for_department"])]) > 900):
                                    y=1
                                else:
                                    if(str(x["known_for_department"]) == "Acting"):
                                        CrewList[str(x["known_for_department"])] = CrewList[ifNull(str(x["known_for_department"]))] +' '+ ifNull(str(x["name"])) +' as '+ ifNull(str(x["character"])) +','
                                    else:
                                        CrewList[str(x["known_for_department"])] = CrewList[ifNull(str(x["known_for_department"]))] +' '+ ifNull(str(x["name"])) +','
                            else:
                                if(str(x["known_for_department"]) == "Acting"):
                                    CrewList[ifNull(str(x["known_for_department"]))] = ifNull(str(x["name"])) +' as '+ ifNull(str(x["character"])) +','
                                else:
                                    CrewList[ifNull(str(x["known_for_department"]))] = ifNull(str(x["name"])) +','
                                
                        
                        title = ifNull(str(OMDBinfo["Title"]))
                        year = ifNull(str(OMDBinfo["Year"]))
                        
                        embed=discord.Embed(color=discord.Color(11812188))
                        embed.set_author(name="Bot Crew Info", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
                        embed.add_field(name="**Title**", value=title, inline=False)
                        embed.add_field(name="**Year**", value=year, inline=True)
                        
                        for key, value in CrewList.items():
                            print(key)
                            print(value[0:len(value)-1])
                            embed.add_field(name="**"+key+"**", value=value[0:len(value)-1], inline=False)
                            
                        if(ifNull(str(movieQueryList[index]["poster_path"])) != "N/A"):
                            imageLink = "https://image.tmdb.org/t/p/original"+str(movieQueryList[index]["poster_path"])
                            embed.set_image(url=imageLink)
                            
                        await ctx.message.channel.send(embed=embed)
                            
                    except KeyError:
                        await botError(ctx, "Bot could not find the requested media...")
            
            except KeyError:
                await botError(ctx, "Bot ran into an issue...")
                return "Something wrong with movie function"
            
    else:
        await botError(ctx, "Bot could not find the requested media...")

async def getTrailer(ctx):
    headerData = {
        'Content-Type': 'application/json'
    }
    
    message = ctx.message.clean_content

    options = find_options(message, [])
    
    returnedMovieQuery = await mediaSearchQuery(options[0])
    movieQueryList = returnedMovieQuery.json()["results"]
    
    if(len(movieQueryList) != 0):
        index = 0
        foundMovie = False
        
        if(len(options) == 2):
            foundMovie = True
            index = int(options[1])
        else:
            while(index < len(movieQueryList) and foundMovie == False):
                if(movieQueryList[index]["media_type"] == "movie"):
                    foundMovie = True
                else:
                    index += 1
                
        if(foundMovie == False):
            await botError(ctx, "Bot could not find the requested media...")
        else:
            try:
                request = requests.get('https://api.themoviedb.org/3/movie/'+str(movieQueryList[index]["id"])+'?api_key='+API_TOKEN_TMDB, headers = headerData)
                TMDBinfo = request.json()
                print(str(TMDBinfo))
                      
                if(TMDBinfo["imdb_id"] is None):
                    try:
                        requestTrailer = requests.get('https://api.themoviedb.org/3/movie/'+str(movieQueryList[index]["id"])+'/videos?api_key='+API_TOKEN_TMDB, headers = headerData)
                        Trailerinfo = requestTrailer.json()
                        print(str(Trailerinfo))

                        title = ifNull(str(TMDBinfo["title"]))
                        
                        if(len(Trailerinfo["results"]) != 0):
                            youtubeTrailers = []
                            for x in Trailerinfo["results"]:
                                if(str(x["site"]) == "YouTube"):
                                    youtubeTrailers.append(str(x["key"]))
                                else:
                                    y=1
                                
                            if(len(youtubeTrailers) != 0):
                                randomTrailer = random.randint(0, len(youtubeTrailers)-1)
                                await ctx.message.channel.send('Here is a trailer for ' +title)
                                await ctx.message.channel.send('https://www.youtube.com/watch?v='+youtubeTrailers[randomTrailer])
                            else:
                                await botError(ctx, "Bot could not find the requested media...")
                        else:
                            await botError(ctx, "Bot could not find the requested media...")
   
                    except KeyError:
                        await botError(ctx, "Bot could not find the requested media...")
                else:
                    try:
                        request = requests.get('http://www.omdbapi.com/?i='+str(TMDBinfo["imdb_id"])+'&plot=full&apikey='+API_TOKEN_OMDB, headers = headerData)
                        requestTrailer = requests.get('https://api.themoviedb.org/3/movie/'+str(movieQueryList[index]["id"])+'/videos?api_key='+API_TOKEN_TMDB, headers = headerData)
                        OMDBinfo = request.json()
                        Trailerinfo = requestTrailer.json()
                        print(str(OMDBinfo))
                        print(str(Trailerinfo))

                        title = ifNull(str(OMDBinfo["Title"]))
                        year = ifNull(str(OMDBinfo["Year"]))
                        
                        if(len(Trailerinfo["results"]) != 0):
                            youtubeTrailers = []
                            for x in Trailerinfo["results"]:
                                if(str(x["site"]) == "YouTube"):
                                    youtubeTrailers.append(str(x["key"]))
                                else:
                                    y=1
                                
                            if(len(youtubeTrailers) != 0):
                                randomTrailer = random.randint(0, len(youtubeTrailers)-1)
                                await ctx.message.channel.send('Here is a trailer for ' +title+ ' ('+year+')')
                                await ctx.message.channel.send('https://www.youtube.com/watch?v='+youtubeTrailers[randomTrailer])
                            else:
                                await botError(ctx, "Bot could not find the requested media...")
                        else:
                            await botError(ctx, "Bot could not find the requested media...")
   
                    except KeyError:
                        await botError(ctx, "Bot could not find the requested media...")
            
            except KeyError:
                await botError(ctx, "Bot ran into an issue...")
                return "Something wrong with movie function"
            
    else:
        await botError(ctx, "Bot could not find the requested media...")
        
async def getStreamSites(ctx):
    headerData = {
        'Content-Type': 'application/json'
    }
    
    message = ctx.message.clean_content

    options = find_options(message, [])
    
    returnedMovieQuery = await mediaSearchQuery(options[0])
    movieQueryList = returnedMovieQuery.json()["results"]
    
    if(len(movieQueryList) != 0):
        index = 0
        foundMovie = False
        errorOptions = False
        
        if(len(options) == 3):
            foundMovie = True
            index = int(options[2])
        elif(len(options) == 2):
            while(index < len(movieQueryList) and foundMovie == False):
                if(movieQueryList[index]["media_type"] == "movie"):
                    foundMovie = True
                else:
                    index += 1
        else:
            foundMovie = True
            errorOptions = True
            
                
        if(foundMovie == False):
            await botError(ctx, "Bot could not find the requested media...")
        elif(errorOptions == True):
            await botError(ctx, "Bot didnt get the correct number of options...")
        else:
            try:
                request = requests.get('https://api.themoviedb.org/3/movie/'+str(movieQueryList[index]["id"])+'?api_key='+API_TOKEN_TMDB, headers = headerData)
                TMDBinfo = request.json()
                print(str(TMDBinfo))
                      
                if(TMDBinfo["imdb_id"] is None):
                    try:
                        requestStream = requests.get('https://api.themoviedb.org/3/movie/'+str(movieQueryList[index]["id"])+'/watch/providers?api_key='+API_TOKEN_TMDB, headers = headerData)
                        Streaminfo = requestStream.json()["results"][options[1].upper()]
                        print(str(Streaminfo))
                        
                        StreamString = ''
                        RentString = ''
                        BuyString = ''
                        
                        if("flatrate" in Streaminfo):
                            for x in Streaminfo["flatrate"]:
                                StreamString = StreamString + x["provider_name"] +', '
                        
                        if("rent" in Streaminfo):
                            for x in Streaminfo["rent"]:
                                RentString = RentString + x["provider_name"] +', '
                        
                        if("buy" in Streaminfo):
                            for x in Streaminfo["buy"]:
                                BuyString = BuyString + x["provider_name"] +', '
                                     
                        title = ifNull(str(TMDBinfo["title"]))
                        
                        embed=discord.Embed(color=discord.Color(11812188))
                        embed.set_author(name="Bot Streaming Info", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
                        embed.add_field(name="**Title**", value=title, inline=False)
                        
                        if(ifNull(StreamString) != "N/A"):
                            embed.add_field(name="**Streaming**", value=StreamString[0:len(StreamString)-2], inline=False)
                        else:
                            embed.add_field(name="**Streaming**", value="N/A", inline=False)
                            
                        if(ifNull(RentString) != "N/A"):
                            embed.add_field(name="**Rent**", value=RentString[0:len(RentString)-2], inline=False)
                        else:
                            embed.add_field(name="**Rent**", value="N/A", inline=False)
                            
                        if(ifNull(BuyString) != "N/A"):
                            embed.add_field(name="**Buy**", value=BuyString[0:len(BuyString)-2], inline=False)
                        else:
                            embed.add_field(name="**Buy**", value="N/A", inline=False)
                            
                        if(ifNull(str(movieQueryList[index]["poster_path"])) != "N/A"):
                            imageLink = "https://image.tmdb.org/t/p/original"+str(movieQueryList[index]["poster_path"])
                            embed.set_image(url=imageLink)
                            
                        await ctx.message.channel.send(embed=embed)
                            
                    except KeyError:
                        await botError(ctx, "Bot could not find the requested media...")
                else:
                    try:
                        request = requests.get('http://www.omdbapi.com/?i='+str(TMDBinfo["imdb_id"])+'&plot=full&apikey='+API_TOKEN_OMDB, headers = headerData)
                        requestStream = requests.get('https://api.themoviedb.org/3/movie/'+str(movieQueryList[index]["id"])+'/watch/providers?api_key='+API_TOKEN_TMDB, headers = headerData)
                        OMDBinfo = request.json()
                        Streaminfo = requestStream.json()["results"][options[1].upper()]
                        print(str(OMDBinfo))
                        print(str(Streaminfo))
                        
                        StreamString = ''
                        RentString = ''
                        BuyString = ''
                        
                        if("flatrate" in Streaminfo):
                            for x in Streaminfo["flatrate"]:
                                StreamString = StreamString + x["provider_name"] +', '
                        
                        if("rent" in Streaminfo):
                            for x in Streaminfo["rent"]:
                                RentString = RentString + x["provider_name"] +', '
                        
                        if("buy" in Streaminfo):
                            for x in Streaminfo["buy"]:
                                BuyString = BuyString + x["provider_name"] +', '
                                     
                        title = ifNull(str(OMDBinfo["Title"]))
                        year = ifNull(str(OMDBinfo["Year"]))
                        
                        embed=discord.Embed(color=discord.Color(11812188))
                        embed.set_author(name="Bot Streaming Info", icon_url="https://cdn.discordapp.com/avatars/redacted/ab88d94557f27cad8cc766a6fa1ebb6a.webp?size=160")
                        embed.add_field(name="**Title**", value=title, inline=False)
                        embed.add_field(name="**Year**", value=year, inline=True)
                        
                        if(ifNull(StreamString) != "N/A"):
                            embed.add_field(name="**Streaming**", value=StreamString[0:len(StreamString)-2], inline=False)
                        else:
                            embed.add_field(name="**Streaming**", value="N/A", inline=False)
                            
                        if(ifNull(RentString) != "N/A"):
                            embed.add_field(name="**Rent**", value=RentString[0:len(RentString)-2], inline=False)
                        else:
                            embed.add_field(name="**Rent**", value="N/A", inline=False)
                            
                        if(ifNull(BuyString) != "N/A"):
                            embed.add_field(name="**Buy**", value=BuyString[0:len(BuyString)-2], inline=False)
                        else:
                            embed.add_field(name="**Buy**", value="N/A", inline=False)
                            
                        if(ifNull(str(movieQueryList[index]["poster_path"])) != "N/A"):
                            imageLink = "https://image.tmdb.org/t/p/original"+str(movieQueryList[index]["poster_path"])
                            embed.set_image(url=imageLink)
                            
                        await ctx.message.channel.send(embed=embed)
                            
                    except KeyError:
                        await botError(ctx, "Bot could not find the requested media...")
            
            except KeyError:
                await botError(ctx, "Bot ran into an issue...")
                return "Something wrong with movie function"
            
    else:
        await botError(ctx, "Bot could not find the requested media...")
        
async def botError(ctx, errorJam):
    embed=discord.Embed(color=discord.Color(11812188))
    await ctx.message.channel.send(errorJam)
    await ctx.message.channel.send(embed=embed)
            
def ifNull(value):
    if(not value or value is None or value == "None" or value == ""):
        return "N/A"
    else:
        return value