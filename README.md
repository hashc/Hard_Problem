# Hard_Problem
Data is based on Stack Overflow.

数据格式均为xml形式，用xml标记<row />来封装每一行数据
- Badges.xml
每一个row包含6个字段： Id, UserId, Name, Date, Class, TagBased

Id="82946" UserId="3718" Name="Teacher" Date="2008-09-15T08:55:03.923" Class="3" TagBased="False" 

- Users.xml
每一个row包含字段Id, Reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, ProfileImageUrl, AccountId 个字段

- Comments.xml
每一个row包含6个字段： Id, PostId, Score, Text, CreationDate, UserId

Id="2" PostId="35314" Score="8" Text="Yeah, I didn't believe it until I created a console app - but good lord!  Why would they give you the rope to hang yourself!  I hated that about VB.NET - the OrElse and AndAlso keywords!" CreationDate="2008-09-06T08:09:52.330" UserId="3" 

- Tags.xml
每一个row包含5个字段： Id, TagName, Count, ExcerptPostId, WikiPostId

Id="1" TagName=".net" Count="283778" ExcerptPostId="3624959" WikiPostId="3607476"

- Votes.xml
每一个row包含4个字段：Id, PostId, VoteTypeId, CreationDate

Id="1" PostId="1" VoteTypeId="2" CreationDate="2008-07-31T00:00:00.000"

- Posts.xml
