from flask import Flask, render_template, request
from urllib.request import urlopen as urReq
from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup as bs
import requests


# pip install -r requirements.txt
app = Flask(__name__)

@app.route("/", methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/review',methods=['GET','POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            # print(flipkart_url)
            res_website = urReq(flipkart_url)
            flipkartPage = res_website.read()
            res_website.close()

            flipkart_html = bs(flipkartPage, "html.parser")
            all_phones = flipkart_html.find_all("div", {"class": "_1AtVbE col-12-12"})
            del all_phones[0:2]
            box = all_phones[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']

            prodRes = requests.get(productLink)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            # print(prod_html)

            commentboxes = prod_html.find_all('div',{'class':"_16PBlm"})

            # filename = searchString + ".csv"
            # fw = open(filename, "w")
            # headers = "Product,Customer_Name, Rating,Heading,Comment \n"
            # # headers = "Product,Customer_Name, Rating,Heading \n"
            # fw.write(headers)
            # fw.close()

            reviews = []

            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    name = "Name Information Not available"

                try:
                    rating = commentbox.div.div.div.div.text

                except:
                    rating = "Rating Information Not available"

                try:
                    commentHeading = commentbox.div.div.div.p.text

                except:
                    commentHeading = "Heading Information Not available"

                try:
                    comments = commentbox.div.div.find_all('div', {'class': ""})
                    custComment = comments[0].div.text


                except:
                    custComment = "Comments information not available"

                mydict = {"Product":searchString, "Customer_Name":name,"Rating":rating,"Heading":commentHeading,"Comment":custComment}
                # mydict = {"Product": searchString, "Customer_Name": name, "Rating": rating, "Heading": commentHeading}
                reviews.append(mydict)
                # print(reviews)

            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

    else:
        return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)