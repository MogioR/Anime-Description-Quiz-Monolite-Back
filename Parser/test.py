import requests

query = "query($userId:Int,$userName:String,$type:MediaType){MediaListCollection(userId:$userId,userName:$userName," \
        "type:$type){lists{name isCustomList isCompletedList:isSplitCompletedList entries{...mediaListEntry}}user{id " \
        "name avatar{large}mediaListOptions{scoreFormat rowOrder animeList{sectionOrder customLists " \
        "splitCompletedSectionByFormat theme}mangaList{sectionOrder customLists splitCompletedSectionByFormat " \
        "theme}}}}}fragment mediaListEntry on MediaList{id mediaId status score progress progressVolumes repeat " \
        "priority private hiddenFromStatusLists customLists advancedScores notes updatedAt " \
        "startedAt{year month day}completedAt{year month day}media{id title{userPreferred romaji english " \
        "native}coverImage{extraLarge large}type format status(version:2)episodes volumes chapters averageScore " \
        "popularity isAdult countryOfOrigin genres bannerImage startDate{year month day}}}"


# Define our query variables and values that will be used in the query request
variables = {
    "userId": 309629,
    "type": "ANIME"
}

url = 'https://graphql.anilist.co'

# Make the HTTP Api request
response = requests.post(url, json={'query': query, 'variables': variables})
print(response.text)