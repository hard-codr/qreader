from qreader import extractor

if __name__ == '__main__':
    url = extractor.cleanup_url('https://www.google.com/search?hl=en&ei=-NkcXKjxCMz-9QPl14KoBw&q=remove+utm+parameters+python&oq=remove+utm+parameters+python&gs_l=psy-ab.3..33i22i29i30.5245.11625..11841...3.0..2.899.7752.0j4j7j2j3j4j1......0....1..gws-wiz.......0j0i71j0i131j0i67j0i22i30j33i21j33i160.ZTVUTpq2O30')
    print(url)
