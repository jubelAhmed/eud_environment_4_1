def newspaper_headlines(p0,p1,p2):
  print(p0,p1,p2)
  
def print_content(what_to_print):
    print(what_to_print)
    result = what_to_print
    # params = what_to_print.split("")
    #print_content((newspaper_headlines('Cricket','2020-6-6','PublishedAt')))
    # newspaper_headlines()
    print("Pring News")
    print(result)
    return result
a  = "print_content((newspaper_headlines('Cricket','2020-6-6','PublishedAt')))"

exec(a)