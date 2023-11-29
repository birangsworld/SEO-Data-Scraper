import pandas as pd
import requests
from bs4 import BeautifulSoup


def sheetToDataFrame(filePath):
    try:
        df = pd.read_csv(filePath)
        return df
    except FileNotFoundError:
        print(f"File Not Found At: {filePath}")
        return None
    except Exception as e:
        print(f"An Error Occured: {e}")
        return None


def requestPage(pageRoute):
    requestResponse = requests.get(pageRoute)

    if requestResponse.status_code == 200:
        pageContent = requestResponse.text
        return pageContent
    else:
        print(
            f"Failed to Retrieve Page Content, Status Code: {requestResponse.status_code}"
        )
        return None


def makeSoup(pageContent):
    soup = BeautifulSoup(pageContent, "html.parser")
    return soup


def extractTitle(soup):
    pageTitle = soup.title.string
    return pageTitle


def extractDescription(soup):
    metaDescription = soup.find("meta", {"name": "description"})["content"]
    return metaDescription


def extractHeadings(soup):
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    allHeadings = []

    for heading in headings:
        headingContent = heading.string
        allHeadings.append(headingContent)

    return allHeadings


def extractTextContent(soup):
    allContentTags = soup.find_all("p")

    allContents = []

    for contentTag in allContentTags:
        content = contentTag.string
        allContents.append(content)

    return allContents


def extractImageAlts(soup):
    allImages = soup.find_all("img", alt=True)

    allImageAlts = []
    
    for image in allImages:
        altText = image["alt"]
        allImageAlts.append(altText)

    return allImageAlts

def extractLinks(soup):
    allLinks = soup.find_all("a")
    linkAnchors = []
    linkDestinations = []

    for link in allLinks:
        linkAnchor = link.string
        linkAnchors.append(linkAnchor)

    for link in allLinks:
        linkDestination = link["href"]
        linkDestinations.append(linkDestination)

    return linkAnchors, linkDestinations


def main():
    # FilePath = input("Path to File: ")
    # DataFrame = SheetToDataFrame(FilePath)
    url = "https://ztcprep.com/ielts"
    pageContent = requestPage(url)
    soup = makeSoup(pageContent)
    title = extractTitle(soup)
    metaDescription = extractDescription(soup)
    headings = extractHeadings(soup)
    contents = extractTextContent(soup)
    imageAlts = extractImageAlts(soup)
    anchorTexts, linkDestinations = extractLinks(soup)
    print(linkDestinations)


main()
