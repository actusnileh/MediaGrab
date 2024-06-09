from pytube import YouTube


def get_information(url):
    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    author = yt.author
    title = yt.title
    return thumbnail_url, author, title
