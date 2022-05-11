using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace logic.Models;
public class Attempt
{
    [Key]
    public int Id { get; set; }
    
    public DateTime SubmissionDate { get; set; }
    public int Grade { get; set; } = 0;
    [Required(AllowEmptyStrings = false, ErrorMessage = "Please enter solution url")]
    public string Link { get; set; } = "";
    public string Output { get; set; } = "";

    [ForeignKey("HwTask")]
    public int TaskId { get; set; }
}