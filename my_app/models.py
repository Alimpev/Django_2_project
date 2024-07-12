from django.db import models

from django.contrib.auth.models import User
from django.db.models import Sum



class Author(models.Model):
    rating_auth = models.IntegerField(default=0)

    author_to_User = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):

# we use AGGREGATE function to count all ratings which are relative to one author
# STEPS :    MODEL ->(class) post ; COLOUMN -> rating_post
# use SUM to count --> use AGGREGATE --> use _SET
# in the end we have to create POST_RATING = 0 and plus it to POST_RAT.GET("POST_RAT") to get the value

        post_rat = self.post_set.aggregate(POST_rat=Sum("rating_post"))
        post_rating = 0
        post_rating += post_rat.get('POST_rat')

# here we use Author_to_User because the model [ (class) comment ] has a "relation_to_USER (Author_to_User)" and our model
# [(class) Author ] has a "relation_to_User" too.
# So, the picture is : AUTHOR - USER - COMMENT

        comm_rat = self.author_to_User.comment_set.aggregate(COM_rat=Sum("rating_comment"))
        comment_rating = 0
        comment_rating += comm_rat.get('COM_rat')


        self.rating_auth = post_rating*3 + comment_rating
        self.save()



class Category(models.Model):
    Name_category = models.CharField(max_length=128, unique=True)




class Post(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=250)
    text_article = models.TextField()
    rating_post = models.IntegerField(default=0)

    ARTICLE = "AR"
    NEWS = "NW"

    POSITION = [
        (ARTICLE, "article"),
        (NEWS, "news")
    ]

    topic_choice = models.CharField(max_length=2, choices=POSITION, default=NEWS)


    post_to_author = models.ForeignKey("Author", on_delete=models.CASCADE)
    post_to_category = models.ManyToManyField("Category", through="PostCategory")


    def like(self):
        self.rating_post += 1
        self.save()


    def dislike (self):
        self.rating_post -= 1
        self.save()


    def preview(self):
        return self.text_article[0:123] + "..."


class PostCategory(models.Model):
    postCategory_to_post = models.ForeignKey("Post", on_delete=models.CASCADE)
    postCategory_to_category = models.ForeignKey("Category", on_delete=models.CASCADE)



class Comment(models.Model):
    text_comment = models.TextField()
    time_com_in = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    comment_to_post = models.ForeignKey("Post", on_delete=models.CASCADE)
    comment_to_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()





