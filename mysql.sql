create database ihome charset=utf8;

use ihome;

# 客户信息表 id 用户名 手机号 密码 真实姓名 身份证号 头像url
# 是否是管理员 创建时间 最后更新时间 isdelete
create table user_info(
ui_id int auto_increment primary key not null comment "客户id",
ui_title varchar(32) not null comment "用户名",
ui_tel varchar(11) not null comment "手机号",
ui_email varchar(128) not null comment "邮箱",
ui_pwd varchar(40) not null comment "密码",
ui_name varchar(32) null comment "实名认证_姓名",
ui_card varchar(20) null comment "实名认证_身份证号",
ui_image varchar(128) null comment "头像链接",
ui_is_admin boolean not null default false comment "是否是管理员",
ui_isDelete boolean not null default false comment "是否注销状态",
ui_ctime datetime not null default current_timestamp comment "创建时间",
ui_utime datetime not null default current_timestamp on update current_timestamp comment "最后更新时间",
unique (ui_title),
unique (ui_tel)
) comment "客户信息表";
# 测试信息 insert into user_info(ui_title,ui_tel,ui_pwd) values(12345,13888888888,12345);
# 测试信息 清空表并重置id truncate table user_info;

# 城市信息 id 城市名 创建时间
create table area_info(
ai_id int auto_increment primary key not null comment "城市id",
ai_name varchar(32) not null comment "城市名",
ai_ctime datetime not null default current_timestamp comment "创建时间"
) comment "城市信息表";

# 房屋信息 id 所属客户 标题 单价 所属城市id 地址 房间数量 房屋面积 房屋户型 可住人数 卧床配置
# 押金数 最少入住时间 最多入住时间 房屋销量 审核状态 是否上线 主图片 创建时间 更新时间 isDelete
create table house_info(
hi_id int auto_increment primary key not null comment "房屋id",
hi_user int not null comment "所属客户id",
hi_title varchar(64) not null comment "房屋标题",
hi_price decimal(6,2) not null default "0" comment "房屋单价",
hi_area int not null comment "所属城市id",
hi_address varchar(512) not null default "" comment "房屋详细地址",
hi_count tinyint not null default "1" comment "房间数量",
hi_acreage int not null default "0" comment "房屋面积",
hi_type varchar(32) not null default "" comment "房屋户型",
hi_num int not null default "1" comment "可容纳人数",
hi_beds varchar(512) not null default "" comment "卧床配置",
hi_deposit decimal(7,2) not null default "0" comment "押金数",
hi_min_day int not null default "1" comment "最少入住天数",
hi_max_day int not null default "0" comment "最长入住天数 0表示无限制",
hi_order_count int not null default "0" comment "房屋销量",
hi_verify tinyint not null default "0" comment "审核状态 0未审核 1审核未通过 2审核通过",
hi_isonline boolean not null default true comment "是否上线",
hi_image varchar(128) null comment "房屋主图片",
hi_ctime datetime not null default current_timestamp comment "创建时间",
hi_utime datetime not null default current_timestamp on update current_timestamp comment "最后更新时间",
hi_isDelete boolean not null default false comment "是否删除",
foreign key(hi_user) references user_info(ui_id),
foreign key(hi_area) references area_info(ai_id)
) comment "房屋信息表";

# 房屋图片 id 所属房屋id image_url 创建时间
create table house_image(
him_id int auto_increment primary key not null comment "房屋图片id",
him_house int not null comment "所属房屋id",
him_image varchar(128) not null comment "房屋图片",
him_ctime datetime not null default current_timestamp comment "创建时间",
foreign key(him_house) references house_info(hi_id)
) comment "房屋图片表";

# 设施类型 id 设施名称 创建时间
create table house_faci_type(
hft_id int auto_increment primary key not null comment "设施类型id",
hft_name varchar(32) not null comment "设施名称",
hft_ctime datetime not null default current_timestamp comment "创建时间"
) comment "设施类型表";

# 配套设施 id 设施类型id 所属房屋id 创建时间
create table house_facilities(
hf_id int auto_increment primary key not null comment "设施id",
hf_type int not null comment "设施类型id",
hf_house int not null comment "所属房屋id",
hf_ctime datetime not null default current_timestamp comment "创建时间",
foreign key(hf_type) references house_faci_type(hft_id),
foreign key(hf_house) references house_info(hi_id)
) comment "配套设施表";

# 订单信息 id 订单客户id 所属房屋id 入住时间 离开时间 入住天数 房屋单价
# 订单金额 订单状态(已下单 已接单/已拒单 已支付 ) 评论 创建时间 更新时间
create table order_info(
oi_id int auto_increment primary key not null comment "订单id",
oi_user int not null comment "下单客户id",
oi_house int not null comment "所属房屋id",
oi_start_day date not null comment "入住日期",
oi_end_day date not null comment "离开日期",
oi_count_day int not null comment "入住天数",
oi_price decimal(6,2) not null comment "房屋单价",
oi_amount decimal(9,2) not null comment "订单总额",
oi_status tinyint not null default "0" comment "订单状态 0待接单 1待支付 2已支付 3待评价 4已完成 5已取消 6拒接单",
oi_comment text null comment "评论/备注",
oi_ctime datetime not null default current_timestamp comment "创建时间",
oi_utime datetime not null default current_timestamp on update current_timestamp comment "最后更新时间",
foreign key(oi_user) references user_info(ui_id),
foreign key(oi_house) references house_info(hi_id)
) comment "订单信息表";

区域数据
insert into area_info(ai_name) values("东城区");
insert into area_info(ai_name) values("西城区");
insert into area_info(ai_name) values("朝阳区");
insert into area_info(ai_name) values("海淀区");
insert into area_info(ai_name) values("昌平区");
insert into area_info(ai_name) values("丰台区");
insert into area_info(ai_name) values("房山区");
insert into area_info(ai_name) values("通州区");
insert into area_info(ai_name) values("顺义区");
insert into area_info(ai_name) values("大兴区");
insert into area_info(ai_name) values("怀柔区");
insert into area_info(ai_name) values("平谷区");
insert into area_info(ai_name) values("密云区");
insert into area_info(ai_name) values("延庆区");
insert into area_info(ai_name) values("石景山区");
insert into area_info(ai_name) values("门头沟区");

设施类型数据
insert into house_faci_type(hft_name) values("无线网络");
insert into house_faci_type(hft_name) values("热水淋浴");
insert into house_faci_type(hft_name) values("空调");
insert into house_faci_type(hft_name) values("暖气");
insert into house_faci_type(hft_name) values("允许吸烟");
insert into house_faci_type(hft_name) values("饮水设备");
insert into house_faci_type(hft_name) values("牙具");
insert into house_faci_type(hft_name) values("香皂");
insert into house_faci_type(hft_name) values("拖鞋");
insert into house_faci_type(hft_name) values("手纸");
insert into house_faci_type(hft_name) values("毛巾");
insert into house_faci_type(hft_name) values("沐浴露、洗发露");
insert into house_faci_type(hft_name) values("冰箱");
insert into house_faci_type(hft_name) values("洗衣机");
insert into house_faci_type(hft_name) values("电梯");
insert into house_faci_type(hft_name) values("允许做饭");
insert into house_faci_type(hft_name) values("允许带宠物");
insert into house_faci_type(hft_name) values("允许聚会");
insert into house_faci_type(hft_name) values("门禁系统");
insert into house_faci_type(hft_name) values("停车位");
insert into house_faci_type(hft_name) values("有线网络");
insert into house_faci_type(hft_name) values("电视");
insert into house_faci_type(hft_name) values("浴缸");
