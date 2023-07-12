# wordpress-export-python
 
## convert-posts.py
This script converts the default XML export from wordpress sites and creates a new XML file inside the folder `./exports` that converts the categories and tags to something that the [Craft plugin FeedMe](https://docs.craftcms.com/feed-me/v4/) can use.

It converts this:
```xml
    <category domain="category" nicename="category-1"><![CDATA[Category 1]]></category>
    <category domain="category" nicename="category-2"><![CDATA[Category 2]]></category>
	<category domain="post_tag" nicename="tag-1"><![CDATA[Tag 1]]></category>
    <category domain="post_tag" nicename="tag-2"><![CDATA[Tag 2]]></category>
```

to this:
```xml
    <Categories>
        <Category>Category 1</Category>
        <Category>Category 2</Category>
    </Categories>
    <Tags>
        <Tag>Tag 1</Tag>
        <Tag>Tag 2</Tag>
    </Tags>
```

## blog-redirects.py
This script creates a CSV file of redirects that is compatible with the [Craft plugin Retour](https://nystudio107.com/docs/retour/) from the default wordpress XML export. The CSV file will be inside the folder `./exports`. 

It takes the `<wp:post_name/>`, which is equivelant to the slug in wordpress, and assumes the new path to blog posts will be under the path `/blog`.

For example, `/post-slug` will redirect to `/blog/post-slug`.

## find-images.py
This script parses the default wordpress XML export for `<content:encoded/>` and will create a text file that reports out the images that are referenced in `<content:encoded/>` inside the folder `./exports`. It will also download all the image locally to the folder `./exports/images/`.