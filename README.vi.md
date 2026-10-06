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

Hỏi agent status trong lúc làm không được làm mất nhiệm vụ gốc. Kết quả kiểm thử
cũ phải được xem lại khi input thay đổi. Tool timeout sau một thao tác ghi phải
được đối chiếu trạng thái trước khi thử lại.

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
