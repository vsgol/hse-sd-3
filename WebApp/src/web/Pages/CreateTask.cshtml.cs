using data_lib;
using logic.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace web.Pages;

public class CreateTask : PageModel
{   
    [BindProperty]
    public HwTask HwTask{get; set;} = new HwTask();
    private readonly HwDbContext _context;

    public CreateTask(HwDbContext context)
    {
        _context = context;
        HwTask.PublicationDate = DateTime.Today;
        HwTask.DeadlineDate = DateTime.Today;
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
        {
            return Page();
        }

        if (HwTask.DeadlineDate < HwTask.PublicationDate)
        {
            ModelState.AddModelError(string.Empty, "Deadline can not be earlier then publication");
            return Page();
        }
        _context.Tasks.Add(HwTask);
        await _context.SaveChangesAsync();
        return RedirectToPage("./Teacher");
    }
    public void OnGet()
    {
        
    }
}