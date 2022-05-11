using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace logic.Models;

public class Comment
{
    [Key]
    public int Id { get; set; }
    
    [Required(AllowEmptyStrings = false, ErrorMessage = "Please enter content")]
    public string Content { get; set; } = "";
    [ForeignKey("Attempt")]
    public int AttemptId { get; set; }
}