import vulkan

# 初始化 Vulkan
instance = vulkan.Instance(application_info=vulkan.ApplicationInfo(
    application_name="Vulkan 示例",
    application_version=(1, 0, 0),
    engine_name="No Engine",
    engine_version=(1, 0, 0),
    api_version=(1, 0, 0)
))

# 获取物理设备
physical_devices = instance.enumerate_physical_devices()
if not physical_devices:
    raise RuntimeError("找不到支持 Vulkan 的 GPU")

# 选择第一个物理设备
physical_device = physical_devices[0]

# 创建逻辑设备
queue_family_index = next(
    index for index, properties in enumerate(physical_device.get_queue_family_properties())
    if properties.queue_flags & vulkan.QUEUE_GRAPHICS_BIT
)

device = physical_device.create_device(
    [vulkan.DeviceQueueCreateInfo(queue_family_index, [1.0])],
    []
)

# 获取队列
queue = device.get_queue(queue_family_index, 0)

# 创建命令池
command_pool = device.create_command_pool(queue_family_index)

# 分配命令缓冲区
command_buffer = command_pool.allocate_command_buffers(1)[0]

# 开始记录命令
command_buffer.begin()

# 记录一些命令（示例）
command_buffer.end()

# 提交命令缓冲区
submit_info = vulkan.SubmitInfo(command_buffers=[command_buffer])
queue.submit([submit_info])
queue.wait_idle()

# 打印 Vulkan 初始化成功
print("Vulkan 初始化成功！")

# 清理资源
command_pool.destroy()
device.destroy()
instance.destroy()
