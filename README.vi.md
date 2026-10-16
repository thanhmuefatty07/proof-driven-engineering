# Proof-Driven Engineering

Skill cho agent lập trình: ưu tiên hiệu năng đo được, kiến trúc phù hợp, kiểm tra
bảo mật đối kháng và bằng chứng nghiệm thu.

[Hướng dẫn đầy đủ](README.md) | [Nội dung skill](skills/proof-driven-engineering/SKILL.md)

## Cách Dùng

```text
Dùng $proof-driven-engineering để hoàn thành yêu cầu này. Bảo toàn hành vi và
quyền truy cập, đo hiệu năng trên workload thực, kiểm tra các trường hợp lỗi,
và chỉ kết luận theo bằng chứng đã chạy.
```

Skill cho phép code và kiến trúc phức tạp khi lợi ích được chứng minh. Nó yêu cầu
agent tìm nút thắt, so sánh baseline, bảo toàn contract, thử phá các giả định,
giữ yêu cầu user qua các lần thay đổi và kiểm tra kết quả tool. Comment kể lại
code được bỏ; chú thích bảo vệ invariant quan trọng và thông tin bản quyền được giữ.

Agent không được bịa tên thư viện, import, hàm, tham số, flag, config hoặc khả năng
hỗ trợ của nền tảng. Trước khi dùng API mới hoặc phụ thuộc phiên bản, phải xác minh
đúng gói, nguồn phát hành, phiên bản đang chạy, tài liệu/source tương ứng và một
kiểm thử tích hợp thực. Không cài gói đoán mò để sửa import; nếu chưa xác minh được,
dùng phương án đã kiểm chứng hoặc báo rõ phần `NOT VERIFIED`.

Hỏi agent status trong lúc làm không được làm mất nhiệm vụ gốc. Kết quả kiểm thử
cũ phải được xem lại khi input thay đổi. Tool timeout sau một thao tác ghi phải
được đối chiếu trạng thái trước khi thử lại.

Từ phiên bản 0.4.2, [hướng dẫn kiểm thử](skills/proof-driven-engineering/references/testing-quality.md)
yêu cầu mỗi kiểm thử nhắm vào lỗi cụ thể, có kết quả kỳ vọng độc lập và đi qua
ranh giới thực phù hợp với kết luận. Agent phải dùng lại coverage có ích, kiểm
chứng test bắt được hành vi sai, báo trung thực phần chưa chạy và hoàn thành
các gate bắt buộc. Số lượng test hoặc test chỉ kiểm tra mock không chứng minh
được chất lượng sản phẩm. Phiên bản 0.4.2 chỉ cho phép hợp nhất hoặc xóa test
khi có bằng chứng về contract, oracle, ranh giới thực và consumer; tên hoặc mã
giống nhau không đủ để kết luận test trùng lặp.
Mutation chỉ dùng như phép thử độ nhạy có mục tiêu: không đặt mutation score thành
ngưỡng nghiệm thu, không sinh mutant hàng loạt; lỗi build, import hoặc collection
không chứng minh test đã phát hiện lỗi hành vi. Mutant tương đương hoặc không liên
quan tới contract không phải lý do để thêm test bám vào chi tiết triển khai.

Trước khi sinh dữ liệu, agent phải xác định nơi tạm, mức phát sinh dự kiến,
dung lượng còn trống, chủ sở hữu và cách thu dọn. Cache build tương thích được
dùng lại; dữ liệu cần giữ phải có lý do và nơi lưu riêng đã cấu hình. Mỗi mốc
đã kiểm chứng cập nhật một bản chốt Markdown ngắn gọn. Đường dẫn ổ đĩa chỉ nằm
trong cấu hình cục bộ; skill công khai không áp đặt ổ D hoặc quota cho mọi máy.

## Cài Đặt

```text
Dùng $skill-installer để cài skills/proof-driven-engineering từ repo
https://github.com/thanhmuefatty07/proof-driven-engineering.
```

Codex hỗ trợ thư mục user `~/.agents/skills`. Skill được bật automatic discovery;
gọi rõ `$proof-driven-engineering` khi cần bảo đảm agent nhận yêu cầu sử dụng.
Có thể thêm [rule ngắn](integrations/AGENTS.fragment.md) vào rules của dự án sau
khi kiểm tra các ràng buộc hiện có.

Skill không thể bảo đảm không còn bất kỳ lỗi nào hoặc mọi dòng code đạt tối ưu
toàn cục. [Trạng thái validation](VALIDATION.md) phân biệt kiểm tra đã chạy với
đánh giá chưa có bằng chứng. Sự cải thiện trên dự án thật cần được đo riêng.
