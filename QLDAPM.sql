
CREATE TABLE Employee (
    ID SERIAL PRIMARY KEY,
    FullName VARCHAR(100),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(15),
    Position VARCHAR(50)
);


CREATE TABLE Project (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Description TEXT,
    StartDate DATE,
    EndDate DATE,
    Duration INT,
    Status VARCHAR(50),
    ProjectCost NUMERIC(15, 2)
);



CREATE TABLE Role (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(100)
);


CREATE TABLE Skill (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(100)
);


CREATE TABLE Employee_Skill (
    EmployeeID INT REFERENCES Employee(ID),
    SkillID INT REFERENCES Skill(ID),
    ProficiencyLevel VARCHAR(50),
    YearsOfExperience INT,
    PRIMARY KEY (EmployeeID, SkillID)
);
CREATE TABLE Employee_Project (
    EmployeeID INT REFERENCES Employee(ID),
    ProjectID INT REFERENCES Project(ID),
    RoleID INT REFERENCES Role(ID),
    StartDate DATE,
    EndDate DATE,
    Salary NUMERIC(15, 2),
    PRIMARY KEY (EmployeeID, ProjectID, RoleID)
);
CREATE TABLE Technology (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);
CREATE TABLE Project_Technology (
    ProjectID INT REFERENCES Project(ID),
    TechnologyID INT REFERENCES Technology(ID),
    PRIMARY KEY (ProjectID, TechnologyID)
);

INSERT INTO Employee (FullName, DateOfBirth,  Gender, Email,  PhoneNumber, Position) VALUES
('Nguyễn Văn An', '1990-05-01', 'Nam', 'an.nguyen@example.com', '0901234567', 'Lập trình viên'),
('Trần Thị Bình', '1988-11-20', 'Nữ', 'binh.tran@example.com', '0902345678', 'Kiểm thử viên'),
('Lê Quốc Cường', '1985-07-15', 'Nam', 'cuong.le@example.com', '0903456789', 'Quản lý dự án'),
('Phạm Minh Dũng', '1992-03-10', 'Nam', 'dung.pham@example.com', '0904567890', 'BA'),
('Đỗ Thị Hà', '1995-12-05', 'Nữ', 'ha.do@example.com', '0905678901', 'UI/UX Designer'),
('Vũ Văn Khoa', '1993-06-18', 'Nam', 'khoa.vu@example.com', '0906789012', 'DevOps'),
('Nguyễn Thị Lan', '1991-09-22', 'Nữ', 'lan.nguyen@example.com', '0907890123', 'Tester'),
('Hoàng Gia Phúc', '1990-08-30', 'Nam', 'phuc.hoang@example.com', '0908901234', 'Backend Developer'),
('Trần Bảo Quỳnh', '1994-02-14', 'Nữ', 'quynh.tran@example.com', '0909012345', 'Frontend Developer'),
('Lê Minh Sơn', '1987-07-07', 'Nam', 'son.le@example.com', '0900123456', 'Architect');

INSERT INTO Project (Name, Description, StartDate, EndDate,  Duration, Status,  ProjectCost) VALUES
('Hệ thống bán hàng online', 'Dự án xây dựng website thương mại điện tử đa ngành cho phép doanh nghiệp 
và cá nhân đăng bán các sản phẩm như quần áo, đồ gia dụng, điện tử... 
Hệ thống hỗ trợ người bán trong việc quản lý kho hàng, đơn hàng, doanh thu, và khuyến mãi. 
Người tiêu dùng có thể tìm kiếm, lọc sản phẩm theo giá, đánh giá, thương hiệu; 
đặt hàng, thanh toán online, và theo dõi trạng thái vận chuyển. 
Mục tiêu là số hóa hoạt động kinh doanh truyền thống và tăng khả năng tiếp cận khách hàng thông qua môi trường số.'
, '2024-01-01', '2024-06-30', '5 tháng', 'Đang thực hiện',50000000),
('Ứng dụng đặt lịch khám', 'App đặt lịch bệnh viện trực tuyến cho phép người dân tra cứu thông tin bệnh viện,
bác sĩ, và đặt lịch khám theo thời gian mong muốn. 
Hệ thống hỗ trợ chọn chuyên khoa, đặt lịch khẩn cấp, nhận thông báo nhắc lịch và đánh giá chất lượng khám chữa bệnh.
Bệnh viện có thể quản lý danh sách khám, giảm tải quầy tiếp nhận, và phân luồng bệnh nhân hiệu quả hơn. 
Mục tiêu là nâng cao trải nghiệm người dùng và hiện đại hóa quy trình đặt khám tại các cơ sở y tế.'
, '2024-03-15', '2024-09-30', '6 tháng', 'Đang thực hiện',80000000),
('CRM quản lý khách hàng', 'Phần mềm CRM cho doanh nghiệp giúp doanh nghiệp quản lý thông tin khách hàng, 
lịch sử giao dịch, phản hồi và chiến dịch marketing. 
Hệ thống tích hợp tự động hóa email, phân loại khách hàng tiềm năng, và tạo báo cáo phân tích hành vi người dùng. 
Mục tiêu là tăng hiệu quả chăm sóc khách hàng, cá nhân hóa trải nghiệm mua sắm 
và gia tăng doanh thu thông qua việc giữ chân khách hàng trung thành.'
, '2024-02-01', '2024-08-01', '6 tháng', 'Hoàn thành',60000000),
('Quản lý nhân sự', 'Hệ thống quản lý nhân sự nội bộ cho doanh nghiệp bao gồm các chức năng như lưu trữ thông tin cá nhân, 
hợp đồng lao động, theo dõi chấm công, tính lương, quản lý phép, và đánh giá hiệu suất. 
Ngoài ra, hệ thống hỗ trợ quy trình tuyển dụng, đào tạo và đề xuất thăng tiến. 
Mục tiêu là số hóa quy trình quản trị nguồn nhân lực, giảm thiểu sai sót 
và tăng tính minh bạch trong quản lý nhân viên.'
, '2023-11-01', '2024-04-30', '6 tháng', 'Hoàn thành',90000000),
('Ứng dụng ngân hàng số', 'Phát triển app mobile banking giúp khách hàng thực hiện các giao dịch tài chính nhanh chóng như kiểm tra số dư, 
chuyển khoản, thanh toán hóa đơn, nạp tiền điện thoại, mở tài khoản tiết kiệm online, và quản lý chi tiêu. 
Hệ thống đảm bảo an toàn bằng xác thực hai lớp, mã OTP và thông báo giao dịch theo thời gian thực. 
Mục tiêu là mang lại sự tiện lợi, bảo mật và hiện đại hóa trải nghiệm ngân hàng truyền thống.'
, '2024-05-01', '2025-01-31', '8 tháng', 'Đang thực hiện',30000000),
('Quản lý kho', 'Dự án xây dựng hệ thống phần mềm quản lý kho giúp doanh nghiệp theo dõi hàng tồn kho, 
quản lý nhập – xuất hàng hóa, phân quyền theo nhân sự, và tự động cảnh báo hàng sắp hết. 
Hệ thống có thể tích hợp với phần mềm bán hàng để đồng bộ số liệu. 
Mục tiêu là nâng cao hiệu quả trong công tác hậu cần, hạn chế thất thoát hàng hóa, và tối ưu dòng tiền vận hành.'
, '2024-03-01', '2024-10-01', '7 tháng', 'Đang thực hiện',120000000),
('Website tin tức', 'Dự án phát triển trang báo điện tử với giao diện hiện đại, dễ sử dụng, 
cho phép người dùng cập nhật tin tức theo từng chuyên mục như thời sự, thể thao, giải trí, khoa học… 
Hệ thống hỗ trợ người viết bài đăng tin tức, chèn ảnh/video, lên lịch xuất bản và quản lý bình luận. 
Người dùng có thể tìm kiếm tin, chia sẻ lên mạng xã hội, và nhận thông báo theo chủ đề yêu thích. 
Mục tiêu là cung cấp thông tin nhanh, chính xác và đa chiều đến người đọc.'
, '2024-01-15', '2024-04-15', '3 tháng', 'Hoàn thành',70000000),
('Game mobile', 'Phát triển trò chơi di động thể loại casual với lối chơi đơn giản, đồ họa bắt mắt, 
và âm thanh sinh động nhằm thu hút người chơi thuộc nhiều độ tuổi. 
Game bao gồm hệ thống nhiệm vụ, phần thưởng, bảng xếp hạng và tính năng mời bạn bè. 
Tích hợp quảng cáo và mua vật phẩm trong game để tạo doanh thu. 
Mục tiêu là giải trí cho người dùng và phát triển thị trường game nội địa.'
, '2024-06-01', '2025-02-28', '9 tháng', 'Đang thực hiện',40000000),
('E-learning platform', 'Xây dựng nền tảng học trực tuyến hỗ trợ giáo viên đăng tải bài giảng, bài tập, 
tổ chức thi, chấm điểm tự động và tương tác với học viên qua video call hoặc diễn đàn. 
Học viên có thể đăng ký khóa học, học mọi lúc mọi nơi, và nhận chứng chỉ sau khi hoàn thành. 
Hệ thống phù hợp với trường học, trung tâm đào tạo, hoặc doanh nghiệp đào tạo nội bộ. 
Mục tiêu là thúc đẩy học tập linh hoạt và giảm chi phí đào tạo.'
, '2023-12-01', '2024-09-30', '10 tháng', 'Đang thực hiện',35000000),
('Hệ thống đặt vé máy bay', 'Ứng dụng hỗ trợ người dùng tìm kiếm chuyến bay, so sánh giá vé giữa các hãng hàng không, 
đặt vé trực tuyến và thanh toán qua nhiều phương thức. 
Người dùng có thể lưu thông tin hành khách, nhận vé điện tử, và theo dõi lịch trình bay. 
Hệ thống hỗ trợ đại lý và khách lẻ, góp phần hiện đại hóa ngành du lịch và tăng sự thuận tiện cho khách hàng.'
, '2024-03-01', '2024-12-31', '1 năm', 'Đang thực hiện',25000000);



INSERT INTO Role (Name) VALUES
('Quản lý dự án'),
('Phân tích nghiệp vụ'),
('Kiến trúc sư phần mềm'),
('Nhà thiết kế UI/UX'),
('Lập trình viên Frontend'),
('Lập trình viên Backend'),
('Kiểm thử viên'),
('DevOps Engineer'),
('Scrum Master'),
('Product Owner');



INSERT INTO Skill (Name) VALUES
('Java'),
('Python'),
('JavaScript'),
('SQL'),
('UI/UX Design'),
('Agile/Scrum'),
('Docker'),
('Kubernetes'),
('PostgreSQL'),
('ReactJS');



INSERT INTO Employee_Skill (EmployeeID, SkillID, ProficiencyLevel, YearsOfExperience) VALUES
(1, 1, 'Giỏi', 3),
(1, 3, 'Trung bình', 2),
(2, 4, 'Tốt', 4),
(3, 6, 'Tốt', 6),
(4, 2, 'Giỏi', 5),
(5, 5, 'Tốt', 3),
(6, 7, 'Tốt', 2),
(6, 8, 'Khá', 1),
(7, 4, 'Tốt', 3),
(9, 10, 'Tốt', 2);

INSERT INTO Employee_Project (EmployeeID, ProjectID, RoleID, StartDate, EndDate, Salary) VALUES
(1, 1, 5, '2024-01-01', '2024-06-30', 20000000), -- Nguyễn Văn An làm Lập trình viên Frontend trong dự án Hệ thống bán hàng online
(2, 1, 7, '2024-01-01', '2024-06-30', 15000000), -- Trần Thị Bình làm Kiểm thử viên trong dự án Hệ thống bán hàng online
(3, 1, 1, '2024-01-01', '2024-06-30', 30000000), -- Lê Quốc Cường làm Quản lý dự án trong dự án Hệ thống bán hàng online
(4, 2, 2, '2024-03-15', '2024-09-30', 25000000), -- Phạm Minh Dũng làm Phân tích nghiệp vụ trong dự án Ứng dụng đặt lịch khám
(5, 2, 4, '2024-03-15', '2024-09-30', 20000000), -- Đỗ Thị Hà làm Nhà thiết kế UI/UX trong dự án Ứng dụng đặt lịch khám
(6, 3, 8, '2024-02-01', '2024-08-01', 22000000), -- Vũ Văn Khoa làm DevOps Engineer trong dự án CRM quản lý khách hàng
(7, 4, 7, '2023-11-01', '2024-04-30', 18000000), -- Nguyễn Thị Lan làm Kiểm thử viên trong dự án Quản lý nhân sự
(8, 5, 6, '2024-05-01', '2025-01-31', 25000000), -- Hoàng Gia Phúc làm Lập trình viên Backend trong dự án Ứng dụng ngân hàng số
(9, 6, 5, '2024-03-01', '2024-10-01', 20000000), -- Trần Bảo Quỳnh làm Lập trình viên Frontend trong dự án Quản lý kho
(10, 7, 3, '2024-01-15', '2024-04-15', 30000000); -- Lê Minh Sơn làm Kiến trúc sư phần mềm trong dự án Website tin tức

INSERT INTO Technology (Name) VALUES
('Java'),
('Python'),
('JavaScript'),
('ReactJS'),
('Node.js'),
('PostgreSQL'),
('Docker'),
('Kubernetes'),
('AWS'),
('Azure');

-- Dữ liệu mẫu cho bảng Project_Technology
INSERT INTO Project_Technology (ProjectID, TechnologyID) VALUES
(1, 3), -- Hệ thống bán hàng online sử dụng JavaScript
(1, 4), -- Hệ thống bán hàng online sử dụng ReactJS
(2, 2), -- Ứng dụng đặt lịch khám sử dụng Python
(3, 6), -- CRM quản lý khách hàng sử dụng PostgreSQL
(3, 7), -- CRM quản lý khách hàng sử dụng Docker
(4, 1), -- Quản lý nhân sự sử dụng Java
(5, 8), -- Ứng dụng ngân hàng số sử dụng Kubernetes
(6, 5), -- Quản lý kho sử dụng Node.js
(7, 9), -- Website tin tức sử dụng AWS
(8, 10); -- Game mobile sử dụng Azure
select * from Employee_Skill
