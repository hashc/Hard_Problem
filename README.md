# Hard_Problem
Data is based on Stack Overflow.

数据格式均为xml形式，用xml标记<row />来封装每一行数据

- Posts.xml
'id', 'posttypeid', 'acceptedanswerid', 'creationdate', 'score', 'viewcount', 'body', 'owneruserid', 'lasteditoruserid', 'lasteditordisplayname', 'lasteditdate', 'lastactivitydate', 'title', 'tags', 'answercount', 'commentcount', 'favoritecount', 'communityowneddate'

Question部分

|label|explaination|
|--|--|
|id,posttypid|questionID, if posttypid=1 |
|acceptedanswerid|被提问者接受的答案ID|
|creationdate|创建时间|
|score|whether it show research effort and is useful and clear,问题质量|
|viewcount|浏览量|
|body|主要内容|
|owneruserid|提问者or回答者|
|lasteditoruserid|最后一个编辑问题的人|
|lasteditordisplayname|最后一个编辑的名字|
|lasteditdate|最后编辑日期|
|lastactivitydate|最后被编辑的时间|
|title|问题的标题|
|tags|问题的tag|
|answercount|回答数|
|commentcount|对问题的评论|
|favoritecount|对问题的收藏数|
|communityowneddate||

Answer部分

|label|explaination|
|--|--|
|id,posttypeid| AnswerId if posttypeid =2|
|parentid|回答对应的QuestionId|
|creationdate||
|score|is useful and clear,回答质量|
|body|内容|
|owneruserid|回答者ID|
|commentcount|评论数|



- Badges.xml 3.71G

每一个row包含6个字段： Id, UserId, Name, Date, Class, TagBased

Id="82946" UserId="3718" Name="Teacher" Date="2008-09-15T08:55:03.923" Class="3" TagBased="False" 

- Users.xml 3.38G

每一个row包含字段Id, Reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, ProfileImageUrl, AccountId 

- Comments.xml 19.5G

每一个row包含6个字段： Id, PostId, Score, Text, CreationDate, UserId

Id="2" PostId="35314" Score="8" Text="Yeah, I didn't believe it until I created a console app - but good lord!  Why would they give you the rope to hang yourself!  I hated that about VB.NET - the OrElse and AndAlso keywords!" CreationDate="2008-09-06T08:09:52.330" UserId="3" 

- Tags.xml 4.96MB

每一个row包含5个字段： Id, TagName, Count, ExcerptPostId, WikiPostId

Id="1" TagName=".net" Count="283778" ExcerptPostId="3624959" WikiPostId="3607476"

- Votes.xml 16.9G

每一个row包含4个字段：Id, PostId, VoteTypeId, CreationDate

Id="1" PostId="1" VoteTypeId="2" CreationDate="2008-07-31T00:00:00.000"

- Posts.xml
'id', 'posttypeid', 'acceptedanswerid', 'creationdate', 'score', 'viewcount', 'body', 'owneruserid', 'lasteditoruserid', 'lasteditordisplayname', 'lasteditdate', 'lastactivitydate', 'title', 'tags', 'answercount', 'commentcount', 'favoritecount', 'communityowneddate'
|--|--|
|
