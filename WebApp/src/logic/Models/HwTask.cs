using System.ComponentModel.DataAnnotations;

namespace logic.Models;

public class HwTask
{
    [Key]
    public int Id { get; set; }
    
    [Required(AllowEmptyStrings = false, ErrorMessage = "Please enter task name")]
    public string Name { get; set; } = "";
    [DataType(DataType.Date)]
    public DateTime PublicationDate { get; set; }
    [Required(AllowEmptyStrings = false, ErrorMessage = "Please enter task description")]
    public string Description { get; set; } = "";
    [DataType(DataType.Date)]
    public DateTime DeadlineDate { get; set; }
}