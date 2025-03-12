from instaloader import Instaloader, Profile

L = Instaloader()
profile = Profile.from_username(L.context, 'archdrawsalot')

print(profile.followers)