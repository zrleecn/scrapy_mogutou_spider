# 蘑菇头表情分页采集器

## 关键字
- 图片下载
- 蘑菇头表情采集
## setting.py

- 配置图片保存的路径 
```
IMAGES_STORE
```



## pipelines.py

```

# 继承 scrapy.pipelines.imagesImagesPipeline
class MogutouspiderPipeline(ImagesPipeline):

    # 读取配置文件IMAGES_STORE
    IMAGES_STORE = settings.get("IMAGES_STORE")

    # 重写方法
    def get_media_requests(self, item, info):
        if item['img_url']:
            image_url = item['img_url']
            yield scrapy.Request(image_url)

    # 重写方法
    def item_completed(self, results, item, info):
        # 获取图片保存路径
        image_path = [x['path'] for ok,x in results if ok]
        # 图片保存路径 自动保存在setting.py 中的IMAGES_STORE 的路径

        # 自定义保存目录
        if not os.path.exists(self.IMAGES_STORE + "/full/" + item['folder']):
            # 创建目录
            os.mkdir(self.IMAGES_STORE + "/full/" + item['folder'])
        # 移动已经保存好的图片
        print("保存"+self.IMAGES_STORE + "/full/" + item['folder'] + "/" + item['img_url'][-14:])
        os.rename(self.IMAGES_STORE + "/" + image_path[0], self.IMAGES_STORE + "/full/" + item['folder'] + "/" + item['img_url'][-14:])



```
