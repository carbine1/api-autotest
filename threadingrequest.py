# 他人成果
import threading, time, httplib, random
# 需要测试的 url 列表，每一次的访问，我们随机取一个
urls = [
	"/test?page=",
	"/test2?orderby=a&page=",
	"/test2?orderby=d&page=",
]
MAX_PAGE = 10000
SERVER_NAME = "192.168.0.64:80"
TEST_COUNT = 10000
# 创建一个 threading.Thread 的派生类
class RequestThread(threading.Thread):
	# 构造函数
	def __init__(self, thread_name):
		threading.Thread.__init__(self)
		self.test_count = 0

	# 线程运行的入口函数
	def run(self):
		# 不直接把代码写在run里面是因为也许我们还要做其他形式的测试
		i = 0
		while i < TEST_COUNT:
			self.test_performace()
			i += 1
		#self.test_other_things()

	def test_performace(self):
		conn = httplib.HTTPConnection(SERVER_NAME)
		# 模拟 Keep-Alive 的访问, HTTP 1.1
		for i in range(0, random.randint(0, 100)):
			# 构造一个 url，提供随机参数的能力
			url = urls[random.randint(0, len(urls) - 1)];
			url += str(random.randint(0, MAX_PAGE))
			# 这就连接到服务器上去
			#print url
			try:
				conn.request("GET", url)
				rsps = conn.getresponse()
				if rsps.status == 200:
					# 读取返回的数据
					data = rsps.read()
				self.test_count += 1
			except:
				continue
			
		conn.close()
		
# main 代码开始

# 开始的时间
start_time = time.time()
threads = []
# 并发的线程数
thread_count = 100 

i = 0
while i < thread_count:
	t = RequestThread("thread" + str(i))
	threads.append(t)
	t.start()
	i += 1
# 接受统计的命令
word = ""
while True:
	word = raw_input("cmd:")
	if word == "s":
		time_span = time.time() - start_time
		all_count = 0
		for t in threads:
			all_count += t.test_count
		print "%s Request/Second" % str(all_count / time_span)
	elif word == "e":
		# 准备退出 其实 X 掉 窗口更加容易，没什么浪费的资源
		TEST_COUNT = 0
		for t in threads:
			t.join(0)
		break	
