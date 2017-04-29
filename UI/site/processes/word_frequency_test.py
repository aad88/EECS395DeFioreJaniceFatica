
from word_frequency import get_most_frequent_words

data = ['League was free. Most games back then required you to purchase the game or pay a monthly subscription. Even "free" games like Runescape needed a subscription for most of the content. There were really only a ton of flash games that were free at that time, essentially. It was pretty easy to get into LoL earlier on as well, like in Season 1/Season 2 (so 5-6 years ago). A lot of growth happened during Season 1.',
'Not a lot of competition. Dota was a bit outdated and Dota 2 wasn\'t out yet. Plus, you needed to have Warcraft 3 to play Dota. There was also Heroes of Newerth, but it wasn\'t a free game at the time. Also, League was pretty similar to the other popular games back in 2010/2011 like Starcraft and WoW. When Starcraft and WoW started losing players because of negative changes, LoL was one of the games people switched to. SC2 e-sports had issues in Korea because for a long time because negotiations between Blizzard and KeSPA, meaning there wasn\'t much interest in Korea for SC2. Other games like Runescape and even console games like Call of Duty lost many players during this time-frame too, a large portion of which went over to League. By the time Dota 2 officially released in 2013, League was already by far and away the biggest game on the PC, too late to be dethroned by Dota 2.',
'LoL was easier to play than HoN, one of its biggest early competitors, but still interesting and engaging to play. It was almost the perfect difficulty for a popular game. Easy enough to play casually, hard enough for competitive or hardcore gamers to enjoy. It appeals to the widest audience.']
#data = ['It was the best of time it was the worst of times']
words = get_most_frequent_words(data)

for word in words:
    print word
