from django.db import models

DISCLOSURE_CHOICES = (
    (0, 'private'),
    (1, 'public')
)

# Create your models here.
class Cfboard(models.Model):
    title = models.CharField(max_length=50,verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    hits = models.IntegerField(default=0, verbose_name='조회수')
    writer = models.ForeignKey('cfuser.Cfuser', on_delete=models.CASCADE,
                               verbose_name='작성자')
    boardname = models.ForeignKey('cfboard.Boardcode', on_delete=models.CASCADE,verbose_name='보드종류')
    catename = models.ForeignKey('cfboard.Boardcate', on_delete=models.CASCADE,verbose_name='카테고리')
    disclosure = models.SmallIntegerField(choices=DISCLOSURE_CHOICES)
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간')
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'coffeeshop board'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'

class Boardcode(models.Model):
    boardname = models.CharField(max_length=50)
    
    def __str__(self):
        return self.boardname
    
    class Meta:
        db_table = 'board name'
        verbose_name = '게시판종류'
        verbose_name_plural = '게시판종류'

class Boardcate(models.Model):
    catename = models.CharField(max_length=50)

    def __str__(self):
        return self.catename
    
    class Meta:
        db_table = 'board category'
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'

class Boardcomment(models.Model):
    board = models.ForeignKey('cfboard.Cfboard', on_delete=models.CASCADE,verbose_name='게시글')
    user = models.ForeignKey('cfuser.Cfuser', on_delete=models.CASCADE, verbose_name='작성자')
    contents = models.TextField(verbose_name='내용')
    

    def __str__(self):
        return self.board.title
    
    class Meta:
        db_table = 'board comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'

