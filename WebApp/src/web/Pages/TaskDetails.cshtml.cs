using data_lib;
using logic.Models;
using logic.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using RabbitMQ.Client;
using System.Text;
using Microsoft.VisualBasic.CompilerServices;

namespace web.Pages;

public class TaskDetails : PageModel
{
    [BindProperty]
    public Attempt Attempt{get; set;} = new Attempt();
    private readonly HwDbContext _context;

    public HwTask HwTask { get; set; }
    
    public TaskDetails(HwDbContext context)
    {
        _context = context;
    }
    
    public async Task<IActionResult> OnGetAsync(int? id)
    {
        if (id == null)
        {
            return NotFound();
        }
        
        HwTask = await _context.Tasks.FirstOrDefaultAsync(m => m.Id == id);

        if (HwTask == null)
        {
            return NotFound();
        }
        return Page();  
    }
    
    public async Task<IActionResult> OnPostAsync(int? id)
    {
        if (id == null)
        {
            return NotFound();
        }
        
        HwTask = await _context.Tasks.FirstOrDefaultAsync(m => m.Id == id);

        if (HwTask == null)
        {
            return NotFound();
        }
        
        Attempt.TaskId = HwTask.Id;
        Attempt.SubmissionDate = DateTime.Now;
        Attempt.Output = "Waiting for checker results";
        
        if (!ModelState.IsValid)
        {
            return Page();
        }

        _context.Attempts.Add(Attempt);
        _context.SaveChanges();

        QueueUtils.SendMessage(Attempt.Id.ToString());
        
        return RedirectToPage("./SubmissionsList");
    }
}